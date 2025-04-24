import sqlite3

#Connecting database
#If database is not found with given name,it will create
conn=sqlite3.connect('url.db')
cursor=conn.cursor()

#sql query to create table with requirements if it doesn't already exist
cursor.execute(''' CREATE TABLE IF NOT EXISTS urls (
        short TEXT PRIMARY KEY,    
        long TEXT NOT NULL,        
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP  
    )''')

#commit changes or saves the table in database
conn.commit()

#close the connection
conn.close()

print("Database created successfully")
