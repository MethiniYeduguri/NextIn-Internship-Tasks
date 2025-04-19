import tkinter as tk
from tkinter import messagebox
import random
import smtplib
from email.message import EmailMessage

def send_otp():
    global generated_otp
    input_email=email_entry.get()

    if not input_email:
        messagebox.showerror("Error","Empty,Please enter you email")
        return

    generated_otp=random.randint(100000,999999)
    sender_email="secretboxhide27@gmail.com"
    app_password="egvq rhcc tbpa slkr"

    try:
        msg=EmailMessage()
        msg.set_content(f"Your One-Time Password (OTP) is: {generated_otp}. Please enter this code to complete your verification. This OTP is valid for 5 minutes")
        msg['Subject']="Your OTP Verification Code"
        msg['From']=sender_email
        msg['To']=input_email

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email,app_password)
        server.send_message(msg)
        server.quit()

        messagebox.showinfo("Success","OTP sent to your email!")

        #revealing Otp field to enter and changing button text
        otp_label.pack(pady=(10,5))
        otp_entry.pack(pady=(0,10))
        send_btn.config(text="Login",command=verify_otp)

    except Exception as e:
        messagebox.showerror("Error",f"Failed to send OTP.\n{e}")

def verify_otp():
    input_otp=otp_entry.get()
    if(input_otp==str(generated_otp)):
        messagebox.showinfo("Verified","OTP was verified successfully")
    else:
        messagebox.showinfo("Invalid","Invalid OTP")

#create the main window
login=tk.Tk()
login.title("Signin through OTP verification")
login.configure(bg="#F5FBFF")
login.geometry("700x700")

#White frame in center
email_frame = tk.Frame(login, bg="white",width=300, height=100,padx=100,pady=150)
email_frame.pack(padx=20,pady=20,anchor='center')


# Centering contents inside white frame using internal frame
inner_frame = tk.Frame(email_frame, bg="white",padx=20,pady=20)
inner_frame.pack(padx=10,pady=10)

#email label
email_label=tk.Label(inner_frame,text="Email", font=("Arial", 10), bg="white")
email_label.pack(pady=(0,5))

#email entry
email_entry=tk.Entry(inner_frame,width=30,bg="#D3D3D3")
email_entry.pack(pady=(0,20))

# Send OTP Button
send_btn = tk.Button(inner_frame, text="Send OTP",command=send_otp, bg="#4285F4", fg="white", width=10)
send_btn.pack(side=tk.BOTTOM, pady=(10, 0), fill=tk.X)

#OTP Label & Entry(Hidden Intially)
otp_label=tk.Label(inner_frame,text="Enter OTP", font=("Arial",10),bg="white")
otp_entry=tk.Entry(inner_frame,width=30,bg="#D3D3D3")

login.mainloop()

