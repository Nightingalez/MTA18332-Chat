from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter

''''This function recieves the messeges'''
def msgRecieve():
    while True:
        try:
            