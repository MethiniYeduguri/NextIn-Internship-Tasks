import tkinter as tk
import winsound
from playsound import playsound

#function to pop sound
def play_click_then(func):
    def combine():
        playsound(r"E:\Nextln Internship\Sounds_CB\pop.mp3")
        func()
    return combine

#animation function
def animate(label,msg,index=0,delay=30):
    if(index<=len(msg)):
        label.config(text=msg[:index])
        chatbot.after(30,lambda:animate(label,msg,index+1,delay))#Speed can be adjusted here
    
def show_main_menu():
    clear_screen()
    tk.Label(chatbot, text="Welcome to Pani Weds Puri!", font=('Helvetica', 16),bg="#DDDBCB").pack(pady=10)

    #empty label to animate welcome text
    greeting_label=tk.Label(chatbot,text="",font=('Helvetica', 12, 'italic'),bg="#DDDBCB",wraplength=250,justify='center',fg="#333",padx=10,pady=10)
    greeting_label.pack(pady=10)
    
    #greeting message
    greeting_msg="Hi! I'm Purika 🍽,your dining assistant at Pani Weds Puri.\nLet’s make your experience delicious!"

    #start animation
    animate(greeting_label,greeting_msg)
    
    chatbot.after(4400,lambda:tk.Button(chatbot, text="Book a Table", command=play_click_then(book_table)).pack(pady=5))
    chatbot.after(4500,lambda:tk.Button(chatbot, text="Browse Menu", command=play_click_then(browse_menu)).pack(pady=5)) 
    chatbot.after(4600,lambda:tk.Button(chatbot, text="Give Feedback", command=play_click_then(feedback)).pack(pady=5))
    
def clear_screen():
    for widget in chatbot.winfo_children():
        widget.destroy()

def book_table():
    clear_screen()
    tk.Label(chatbot, text="Select number of guests:",bg="#DDDBCB").pack()
    for i in range(1, 6):
        tk.Button(chatbot, text=str(i), command=lambda i=i: confirm_booking(i)).pack(pady=2)
    tk.Button(chatbot, text="Back", command=play_click_then(show_main_menu)).pack(pady=10)

def confirm_booking(guests):
    clear_screen()
    tk.Label(chatbot, text=f"Table for {guests} booked successfully!",bg="#DDDBCB").pack(pady=10)
    tk.Button(chatbot, text="Main Menu", command=play_click_then(show_main_menu)).pack()

# Placeholder functions for other features
def browse_menu():
    clear_screen()
    order_label=tk.Label(chatbot,text="",font=('Helvetica', 12, 'italic'),bg="#DDDBCB",wraplength=250,justify='center',fg="#333",padx=10,pady=10)
    order_label.pack(pady=10)
    order_msg=("Go through the menu. Select the items of your choice. Then click on order food")
    animate(order_label,order_msg)
    
    menu=[("Pani Puri", 30),
        ("Masala Puri", 40),
        ("Dahi Puri", 35),
        ("Bhel Puri", 25),
        ("Kachori", 25),
        ("Samosa Chat", 50),
        ("Papdi Chat", 35)]
    # Dictionary to store variables for each item
    global order_list
    order_list = {}
    
    for i,(item,price) in enumerate(menu):
        var = tk.IntVar()
        quantity_var = tk.IntVar(value=1)  # Default quantity is 1
        order_list[item] = (var, price, quantity_var)
        check = tk.Checkbutton(chatbot, text=f"{item}-₹{price}",bg="#DDDBCB", variable=var)
        check.pack(anchor='w')
        tk.Spinbox(chatbot, from_=1, to=10, textvariable=quantity_var, width=5).pack(anchor='e', padx=20)
    tk.Button(chatbot,text="Order Food",command=play_click_then(order_food)).pack(pady=10)

#billing the order list
def order_food():
    clear_screen()
    tk.Label(chatbot,text="Your Bill ",font=('Helvetica', 14, 'bold'),bg="#DDDBCB",wraplength=250,justify='center',fg="#333",padx=10,pady=10).pack(pady=10)
    bill_items=""

    amount=0
    for item,(var,price,quantity_var) in order_list.items():
        if(var.get()):#checks whether checkbox is selected
            quantity = quantity_var.get()
            item_total = price * quantity
            bill_items += f"{item}-₹{price} x {quantity} = ₹{item_total}\n"
            amount += item_total

    if(bill_items==""):
        bill_items="No items were selected"
    else:
        bill_items+=f"\n Amount to be paid:₹{amount}"

    tk.Label(chatbot, text=bill_items, font=('Helvetica', 12), bg="#DDDBCB",justify='left').pack(pady=10)

    tk.Button(chatbot, text="Main Menu", command=play_click_then(show_main_menu)).pack(pady=10)
            
def feedback():
    clear_screen()

    #empty label to feedback
    feedback_label=tk.Label(chatbot,text="",font=('Helvetica', 14, 'bold'),bg="#DDDBCB",wraplength=250,justify='center',fg="#333",padx=10,pady=10)
    feedback_label.pack(pady=20)

    #feedback text
    feedback_msg="How was your experience?"

    animate(feedback_label,feedback_msg)

    feedback_var=tk.IntVar(value=0)
    #feedback options
    options = [
        ("Excellent🤩", 1),
        ("Good 🙂", 2),
        ("Average 😐", 3),
        ("Poor 😕", 4),
        ("Very Poor 😡", 5)
    ]

    for i, (text, value) in enumerate(options):
        tk.Radiobutton(
            chatbot,
            text=text,
            font=('Arial', 12),
            bg="#DDDBCB",
            variable=feedback_var,
            value=value,
            command=play_click_then(lambda v=value: feedback_response(feedback_label, v))
        ).pack(pady=5)
    
#function for answering feedback
def feedback_response(label,num):
    if(num==1):
        label.config(text="Thank you for your wonderful feedback! 🌟 We’re thrilled you loved it!")
    elif(num==2):
        label.config(text="Thanks! 😊 We’re glad you had a good experience.")
    elif(num==3):
        label.config(text="Thanks for your feedback. We'll work on making it even better! 👍")
    elif(num==4):
        label.config(text="We're sorry to hear that. 😔 We'll strive to improve!")
    else:
        label.config(text="We sincerely apologize. 😢 Your feedback will help us do better.")
    tk.Button(chatbot, text="Main Menu", command=play_click_then(show_main_menu)).pack(pady=10)

#Tkinter setup
chatbot= tk.Tk()
chatbot.title("Pani Weds Puri Takeaway")
chatbot.config(bg="#DDDBCB")

# Center the window
screen_width = chatbot.winfo_screenwidth()
screen_height = chatbot.winfo_screenheight()
window_width = 350  # As set in geometry
window_height = 500  # As set in geometry
x = (screen_width - window_width) // 2
y = (screen_height - window_height) // 2
chatbot.geometry(f"{window_width}x{window_height}+{x}+{y}")

show_main_menu()
chatbot.mainloop()
