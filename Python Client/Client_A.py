from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter

'''The following functions deal with recieveng and sending messeges in the client'''

'''This function recieves the messeges'''
def msgRecieve():
    while True:
        try:
            msg = client_scoket.recv(BUFSIZ).decode("utf8") #Stops execution of the loop until a message is recieved
            msgList.insert(tkinter.END, msg) #A list which holds the recieved message
        except OSError:
            break

'''This function sends the messeges'''
def msgSend(event = None):
    msg = myMsg.get()
    myMsg.set("")
    client_socket.send(bytes(msg, "utf8"))
    if msg == "{Quit}":
        client_socket.close()
        top.quit()

'''This function closes the socket before the GUI gets closed'''
def scktClose(event = None):
    myMsg.set("{Quit}") #The input field is set to {Quit}
    msgSend() #The msgSend funciton, defined above, gets called and executed

'''GUI build'''

top = tkinter.Tk() #Defines a Tkinter Top-level Widget
top.title("Chat") #Sets the title for it

msgFrame = tkinter.Frame(top) #Groups all other widgets into a complex layout
myMsg = tkinter.StringVar() #A Tkinter string which holds the message that is sent
myMsg.set("Type a message")
sb = tkinter.Scrollbar(msgFrame) #Creates a scrollbar for the frame, so the user can navigate through previous messages

msgList = tkinter.Listbox(msgFrame, height = 30, width = 60, yscrollcommand = sb.set) #Defines a message list, which will hold the messeges
sb.pack(side = tkinter.RIGHT, fill = tkinter.Y) #Placement of the scrollbar
msgList.pack(side = tkinter.LEFT, fill = tkinter.BOTH) #Placement of the list
msgList.pack()
msgFrame.pack()

chatEntry = tkinter.Entry(top, textvariable = myMsg)
chatEntry.bind("<Return>", msgSend) #Sends the message when the user presses Return/Enter
chatEntry.pack()
sendButton = tkinter.Button(top, text = "Send message", command = msgSend) #Creates a "Send message" button in case the user wants to use a button
sendButton.pack()

top.protocol("WM_DELETE_WINDOW", scktClose)

'''Connecting the client to the server'''

HOST = input('Enter host (IP): ')
PORT = input('Enter port: ')

if not PORT:
    PORT = 33000 #This is the default value for the port
else:
    PORT = int(PORT)

BUFSIZ = 1024
ADDR = (HOST, PORT)
client_scoket = socket(AF_INET, SOCK_STREAM)
client_scoket.connect(ADDR)

receive_thread = Thread(target = msgRecieve)
receive_thread.start()
tkinter.mainloop() #Executes the GUI