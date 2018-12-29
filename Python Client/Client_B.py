from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter

def receive():
    while True:
        try:
            message = client_socket.recv(BUFSIZ).decode("utf8")
            message_list.insert(tkinter.END, message)
        except OSError: # Client has left the chat.
            break

def send(event=None):
    msg = my_message.get()
    my_message.set("")
    client_socket.send(bytes(msg, "utf8"))
    if msg == "{quit}":
        client_socket.close()
        top.quit()

def on_closing(event=None):
    my_message.set("{quit}")
    send()

top = tkinter.Tk()
top.title("Chatter")

messages_frame = tkinter.Frame(top)
my_message = tkinter.StringVar()
my_message.set("Type your message: ")
scrollbar = tkinter.Scrollbar(messages_frame)

message_list = tkinter.Listbox(messages_frame, height=15, width=50, yscrollcommand = scrollbar.set)
scrollbar.pack(side = tkinter.RIGHT, fill = tkinter.Y)
message_list.pack(side = tkinter.LEFT, fill = tkinter.BOTH)
message_list.pack()

messages_frame.pack()

entry_field = tkinter.Entry(top, textvariable = my_message)
entry_field.bind("<Return>", send)
entry_field.pack()
send_button = tkinter.Button(top, text = "Send", command = send)
send_button.pack()

top.protocol("WM_DELETE_WINDOW", on_closing)

HOST = input('Enter host: ')
PORT = input('Enter port: ')

if not PORT:
    PORT = 33000
else:
    PORT = int(PORT)

BUFSIZ = 1024
ADDR = (HOST, PORT)
client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(ADDR)

receive_thread = Thread(target=receive)
receive_thread.start()
tkinter.mainloop()