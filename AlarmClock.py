import tkinter as tk
from tkinter import messagebox
from datetime import datetime, timedelta
import math
import threading
from playsound import playsound

# Create the main window
clock = tk.Tk()
clock.title("Alarm Clock")
clock.configure(bg="white")
clock.geometry("700x700")

# Canvas for clock with limited expansion
canvas = tk.Canvas(clock, width=700, height=300, bg="white")
canvas.pack(pady=(0, 20))

def draw_clock(canvas, center_x, center_y, radius):
    canvas.create_oval(center_x - radius - 10, center_y - radius - 10,
                       center_x + radius + 10, center_y + radius + 10,
                       fill="lavender", outline="#D3D3D3", width=1)
    for hour in range(1, 13):
        angle = math.radians((hour / 12) * 360)
        x = center_x + (radius - 5) * math.sin(angle)
        y = center_y - (radius - 5) * math.cos(angle)
        canvas.create_text(x, y, text=str(hour), font=("Arial", 14, "bold"))

def draw_hand(canvas, center_x, center_y, angle_deg, length, width=3, color="black"):
    angle_rad = math.radians(angle_deg)
    x = center_x + length * math.sin(angle_rad)
    y = center_y - length * math.cos(angle_rad)
    canvas.create_line(center_x, center_y, x, y, width=width, fill=color, tags="hands")

def update_clock(center_x, center_y):
    canvas.delete("hands")
    now = datetime.now()
    hour = now.hour % 12
    minute = now.minute
    second = now.second
    hour_angle = (hour + minute / 60) * 30
    minute_angle = (minute + second / 60) * 6
    second_angle = second * 6
    draw_hand(canvas, center_x, center_y, hour_angle, 50, 6, "black")
    draw_hand(canvas, center_x, center_y, minute_angle, 70, 4, "white")
    draw_hand(canvas, center_x, center_y, second_angle, 90, 2, "#D3D3D3")
    canvas.after(1000, lambda: update_clock(center_x, center_y))

# Center of clock face
center_x = 350
center_y = 150
draw_clock(canvas, center_x, center_y, 100)
update_clock(center_x, center_y)

# ================= ALARM FUNCTIONALITY ====================

try:
    # Input Frame placed just below the clock
    alarm_frame = tk.Frame(clock, bg="white")
    alarm_frame.pack(pady=(10, 20))

    # Debug label to confirm frame position
    tk.Label(alarm_frame, text="Alarm Section", bg="white").grid(row=1, column=0, columnspan=7, pady=5)

    alarm_list_frame = tk.Frame(clock, bg="white")
    alarm_list_frame.pack(pady=10)

    tk.Label(alarm_list_frame, text="⏰ Alarms Set:", font=("Arial", 12, "bold"), bg="white").pack()

    # Listbox to show all alarms
    alarm_listbox = tk.Listbox(alarm_list_frame, width=20, font=("Arial", 10))
    alarm_listbox.pack()

    tk.Label(alarm_frame, text="Set Alarm (HH:MM:SS):", font=("Arial", 12), bg="white").grid(row=0, column=0, padx=5)

    alarm_hour = tk.Entry(alarm_frame, width=5)
    alarm_hour.grid(row=0, column=1, padx=2)

    tk.Label(alarm_frame, text=":", bg="white").grid(row=0, column=2)

    alarm_minute = tk.Entry(alarm_frame, width=5)
    alarm_minute.grid(row=0, column=3, padx=2)

    tk.Label(alarm_frame, text=":", bg="white").grid(row=0, column=4)

    alarm_second = tk.Entry(alarm_frame, width=5)
    alarm_second.grid(row=0, column=5, padx=2)

    # List to store alarms and their notification status
    alarm_times = []  # Each entry: (datetime, notified)

    def give_time():
        print("give_time called")
        if not all([alarm_hour.get(), alarm_minute.get(), alarm_second.get()]):
            clock.focus_force()
            messagebox.showerror("Invalid Input", "All fields must be filled!")
            print("Empty input detected")
            return
        try:
            hour = alarm_hour.get().zfill(2)
            minute = alarm_minute.get().zfill(2)
            second = alarm_second.get().zfill(2)
            valid_time = datetime.strptime(f"{hour}:{minute}:{second}", "%H:%M:%S").time()
            print(f"Valid time set: {valid_time}")
            set_alarm(valid_time)
            # Clear input fields
            alarm_hour.delete(0, tk.END)
            alarm_minute.delete(0, tk.END)
            alarm_second.delete(0, tk.END)
        except ValueError as e:
            clock.focus_force()
            messagebox.showerror("Invalid Input", "Please enter valid numbers in HH:MM:SS format (e.g., 13:45:00).")
            print(f"Input error: {e}")

    def set_alarm(valid_time):
        now = datetime.now()
        alarm_time = datetime.combine(now.date(), valid_time)

        if alarm_time <= now:
            alarm_time += timedelta(days=1)

        # Store alarm with notified=False
        alarm_times.append((alarm_time, False))
        alarm_listbox.insert(tk.END, alarm_time.strftime("%H:%M:%S"))
        print(f"Alarm set for {alarm_time}")
        messagebox.showinfo("Reminder", f"Alarm set for {alarm_time}")

        # Start checking alarms if not already running
        if len(alarm_times) == 1:  # Only start if this is the first alarm
            check_alarms()

    def trigger_alarm(alarm_time):
        clock.focus_force()
        threading.Thread(target=play_sound).start()
        messagebox.showinfo("Alarm", f"⏰ It's time to wake up! Get ready to start the day!")
        print("Alarm triggered!")
        # Remove the alarm from alarm_listbox
        alarm_str = alarm_time.strftime("%H:%M:%S")
        if alarm_str in [alarm_listbox.get(i) for i in range(alarm_listbox.size())]:
            idx = [alarm_listbox.get(i) for i in range(alarm_listbox.size())].index(alarm_str)
            alarm_listbox.delete(idx)
            print(f"Removed alarm {alarm_str} from listbox")

    def play_sound():
        try:
            playsound(r"c:/Windows/Media/Alarm05.wav")
            print("Sound played successfully")
        except Exception as e:
            clock.focus_force()
            messagebox.showerror("Sound Error", f"Failed to play sound: {e}")
            print(f"Sound error: {e}")

    def check_alarms():
        now = datetime.now().replace(microsecond=0)
        tolerance = timedelta(seconds=1)  # 1-second tolerance

        # Process alarms
        i = 0
        while i < len(alarm_times):
            alarm_time, notified = alarm_times[i]
            time_diff = (alarm_time - now).total_seconds()

            # Check if alarm should trigger
            if -tolerance.total_seconds() <= time_diff <= 0:
                # Remove alarm before triggering to prevent re-triggering
                alarm_times.pop(i)
                trigger_alarm(alarm_time)
                continue

            # Show notification if within 5 minutes and not notified
            if 0 < time_diff <= 300 and not notified:
                clock.focus_force()
                messagebox.showinfo("Reminder", f"The {alarm_time.strftime('%H:%M:%S')} alarm will ring soon")
                print(f"Reminder shown for {alarm_time}")
                # Mark as notified
                alarm_times[i] = (alarm_time, True)
                i += 1
                continue

            i += 1

        # Schedule next check if there are still alarms
        if alarm_times:
            clock.after(1000, check_alarms)

    tk.Button(alarm_frame, text="Set Alarm", font=("Arial", 10, "bold"), bg="#ADD8E6", command=give_time).grid(row=0, column=6, padx=10)

except Exception as e:
    print(f"Error during widget creation: {e}")
    clock.focus_force()
    messagebox.showerror("Startup Error", f"Failed to initialize GUI: {e}")

# Start GUI
clock.mainloop()
