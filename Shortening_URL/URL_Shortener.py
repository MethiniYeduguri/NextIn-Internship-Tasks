import random
import string
import sqlite3
import tkinter as tk
from tkinter import messagebox
import webbrowser

#generating short url
def generate_short_url():
    #getting long url input
    long_url=long_url_entry.get()
    if not long_url:
        messagebox.showerror("No URL","Please enter a URL")
        return

    #shortening the long url
    short_form=''.join(random.choices(string.ascii_letters+string.digits,k=6))

    #inserting the urls in database
    try:
        conn = sqlite3.connect('urls.db')
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS urls (
                short TEXT PRIMARY KEY,
                long TEXT NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        cursor.execute('INSERT INTO urls (short, long) VALUES (?, ?)', (short_form, long_url))
        conn.commit()
        conn.close()

        # Display short URL
        short_url = f"http://short.ly/{short_form}"
        short_url_label.config(text=f"Short URL: {short_url}")
        #now displaying copy button
        copy_btn.pack(pady=(0, 10))

    except Exception as e:
        messagebox.showerror("Error", f"Failed to shorten URL.\n{e}")

#copy the short url
def copy_url():
    short_url=short_url_label.cget("text").replace("Short URL","")
    if short_url:
        shortener.clipboard_clear()
        shortener.clipboard_append(short_url)
        messagebox.showinfo("Copied", "Short URL copied to clipboard!")

#making the short urls workable
def open_short_url(event):
    short_url = short_url_label.cget("text").replace("Short URL: ", "")
    conn = sqlite3.connect('urls.db')
    cursor = conn.cursor()
    cursor.execute("SELECT long FROM urls WHERE short=?", (short_url.split('/')[-1],))
    result = cursor.fetchone()
    conn.close()
    
    if result:
        webbrowser.open(result[0])
    else:
        messagebox.showerror("Error", "URL not found.")
        
#create the main window
shortener=tk.Tk()
shortener.title("URL Shortening")
shortener.configure(bg="#EEECF3")
shortener.geometry("700x700")

#White frame in center
url_frame = tk.Frame(shortener, bg="white",width=300, height=100,padx=100,pady=150)
url_frame.pack(padx=20,pady=20,anchor='center')


# Centering contents inside white frame using internal frame
inner_frame = tk.Frame(url_frame, bg="white",padx=20,pady=20)
inner_frame.pack(padx=10,pady=10)

#long url label
long_url_label=tk.Label(inner_frame,text="Enter URL To short it", font=("Arial", 10), bg="white")
long_url_label.pack(pady=(0,5))

#long url entry
long_url_entry=tk.Entry(inner_frame,width=30,bg="#D3D3D3")
long_url_entry.pack(pady=(0,20))

#Short Button
short_btn = tk.Button(inner_frame, text="Short It", command=generate_short_url,bg="#4285F4", fg="white", width=10)
short_btn.pack(side=tk.BOTTOM, pady=(10, 0), fill=tk.X)

#Short Label(Hidden Intially)and making the url clickable
short_url_label=tk.Label(inner_frame,text="", font=("Arial",10),bg="white")
short_url_label.pack(pady=10)
short_url_label.bind("<Button-1>", open_short_url)
short_url_label.config(fg="blue", cursor="hand2")

#button to copy the short url
copy_btn = tk.Button(inner_frame, text="Copy URL", bg="#34A853", fg="white", command=copy_url)


shortener.mainloop()
