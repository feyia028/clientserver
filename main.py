import socket
import threading 
from tkinter import *
import mysql.connector
import time

db = mysql.connector.connect( #Connection to the database is establisheded
    host="localhost",
    user="root",
    passwd="XXX",
    port="3306",
    database = "MessagingApp"
)

mycursor = db.cursor() #Cursor which allows me to execute sql querys      

HOST = '127.0.0.1' 
PORT = 9090

class Client():
    
        def __init__(self, host, port):

                self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.sock.connect((host, port)) #Connects to the server

                msg = tkinter.Tk() #Message window
                msg.withdraw()

                self.displayname = simpledialog.askstring("Query", "Please choose a display name", parent = msg)
                #Asks the user for a display name
                self.gui_done = False #Set to False until the GUI has been made
                self.running = True

                gui_thread = threading.Thread(target = self.gui_loop) #Runs throught the gui loop function
                receive_thread = threading.Thread(target = self.receive) #Runs the receive function

                gui_thread.start()
                receive_thread.start()

        def gui_loop(self):
                self.win = tkinter.Tk()
                self.win.configure(bg = "grey") #Background of the window
                self.win.title('Central Messaging System') #Title of the window

                self.chat_label = tkinter.Label(self.win, text = "ChatSpace:", bg = "grey", fg = "black")
                self.chat_label.config(font = ("Calibri", 13))
                self.chat_label.pack(padx = 20, pady = 5)

                self.text_space = tkinter.scrolledtext.ScrolledText(self.win) #Allows the suer to scoll down through chats
                self.text_space.pack(padx = 20, pady = 5)
                self.text_space.config(state = 'disabled') #This is disabled so that the user cannot put text in the text space

                self.msg_label = tkinter.Label(self.win, text = "Message:", bg = "grey", fg = "black")
                self.msg_label.config(font = ("Calibri", 13))
                self.msg_label.pack(padx = 20, pady = 5)

                self.input_space = tkinter.Text(self.win, height = 3)
                self.input_space.pack(padx = 20, pady = 5)

                self.send_button = tkinter.Button(self.win, text = "Send", bg = "grey", fg = "black", command = self.write)
                self.send_button.config(font = ("Calibri", 13)) #Self.write function is called
                self.send_button.pack(padx = 20, pady = 5)

                self.gui_done = True #Set to True as the gui has been built

                self.win.protocol("WM_DELETE_WINDOW", self.stop) #When the window is closed, the program stops
                
                self.win.mainloop()

        def write(self):
                message = f"{self.displayname}: {self.input_space.get('1.0', 'end')}" #Formats the string to show the displayname/message
                self.sock.send(message.encode('utf-8')) #The user message is encoded in utf-8
                self.input_space.delete('1.0', 'end') #Deletes the message from the text space once sent

        def stop(self):
                self.running = False 
                self.win.destroy()
                self.sock.close() #Closes the connection
                exit(0)

        def receive(self):
                while self.running:
                        try:
                                message = self.sock.recv(1024).decode('utf-8') #Receives message from the server
                                if message == 'Please enter your display name': #Checks if the message is equal to the nickname
                                        self.sock.send(self.displayname.encode('utf-8'))
                                else:
                                        if self.gui_done: #Checks if the gui is built
                                                self.text_space.config(state = 'normal') #Allows the text space to be edited
                                                self.text_space.insert('end', message) #Appends the user message to the end
                                                self.text_space.yview('end') #Users will go down with the messages
                                                self.text_space.config(state = 'disabled')
                        except ConnectionAbortedError:
                                break
                        except:
                                print("There is an error with the system.")
                                self.sock.close()
                                break

def register():
    global username #Global variable so that it can be used in the savedata function
    global password #Global variable so that it can be used in the savedata function
    page1 = Toplevel(page) #Leads from the main screen page
    page1.title("Register")
    page1.geometry("500x250") #Size of the window
    
    username = StringVar() #User enter a username which is taken as a string variable
    password = StringVar() #User enters a password which is taken as a string variable
    
    Label(page1, text = "Please create a username and password below:").pack()
    Label(page1, text = "").pack()
    Label(page1, text = "Username:").pack()
    Entry(page1, textvariable = username).pack() #The username is entered in this space
    Label(page1, text = "Password:").pack()
    Entry(page1, textvariable = password).pack() #The password is entered in this space
    Label(page1, text = "").pack()
    Button(page1, text = "Confirm", width = "10", height = "2", command = savedata).pack() #Save data function is eecuted when pressed
    
def savedata():
    user_entry = username.get() #Retrieves the username from the register function
    pass_entry = password.get() #Retrieves the username from the register function
    sql = "INSERT INTO UserDetails (username, password) VALUES (%s, %s)" #SQL query for entering username and password into UserDetails
    mycursor.execute(sql,[(user_entry), (pass_entry)]) #The placeholders %s are replaced by user_entry and pass_entry
    db.commit() #Commited to the database
    messagebox.showinfo("Information", "Details Confirmed!") #Pop up box confirms the details have been appended to the table

def login():
    global enter_user #Global variable so that it can be used in the login_confirm function
    global enter_pass #Global variable so that it can be used in the login_confirm function
    page2 = Toplevel(page) #Leads from the main screen page
    page2.geometry("500x250")
    
    enter_user = StringVar() #User username input is taken as a string
    enter_pass = StringVar() #User password input is taken as a string
    
    Label(page2, text = "Please enter your login details below:").pack()
    Label(page2, text = "").pack()
    Label(page2, text = "Username").pack()
    Entry(page2, textvariable = enter_user).pack() #Username is entered in this spance
    Label(page2, text = "Password").pack()
    Entry(page2, textvariable = enter_pass, show = "*").pack() #Password is entered in this space
    Label(page2, text = "").pack()
    Button(page2, text = "Login", width = "10", height = "2", command = login_confirm).pack() #Login_confirm function is ran when pressed
    
def login_confirm():
    user_confirm = enter_user.get() #Username is passed from login function
    pass_confirm = enter_pass.get() #Password is passed from the login function
    sql = "SELECT * FROM UserDetails WHERE username = %s AND password = %s" #SQL query which checks if the username/password is present
    mycursor.execute(sql,[(user_confirm), (pass_confirm)]) #The placeholders %s are replaced by user_confirm/pass_confirm
    results = mycursor.fetchall() #Fetches all the results which match with what the user typed in
    for i in results:
        messagebox.showinfo("Information", "Successful! Please wait a moment...") #Pop up box which shows succcessful login
        time.sleep(2)
        client = Client(HOST, PORT) #Runs the client as an object
        break
    else:
        messagebox.showinfo("Information", "Incorrect details!") #Pop up box which shows unsuccessful login
            
def main_menu():
    global page #Page variable is global so it can be accessed from other functions
    page = Tk()
    page.geometry("500x250") #The size of the main menu window
    page.title("WELCOME TO THE INSTANT MESSAGING APP!")
    Label(text = "Main Menu", bg = "grey", width = "100", height = "2", font = ("Calibri", 13)).pack()
    Label(text = "").pack()
    Button(text = "Register", height = "2", width = "30", command = register).pack() #The register function is executed when pressed
    Label(text = "").pack()
    Button(text = "Login", height = "2", width = "30", command = login).pack() #The login function is executed when button is pressed
    
    page.mainloop()
    
    
if __name__ == '__main__':
    print(main_menu())
    

    
