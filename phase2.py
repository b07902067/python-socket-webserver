from socket import *
import _thread
import time
import sys
import pickle
import json
from reqfunc import *
from urllib.parse import unquote

HOST = '0.0.0.0'
PORT = 8000


def handleReq(client_socket, method, fileName, body, cookie, cookieMsg):
    if method == "POST":
        if fileName == "/index.html":
            if cookie == True and body != "" :
                # logout first to login
                client_socket.send(b'HTTP/1.1 404 Not Found\r\n')
                client_socket.send(b'Content-Type: text/html\r\n\r\n')
                client_socket.send(b'<html><head></head><body><h1>logout first to login</h1></body></html>\r\n')
            else :
                sendIndex(client_socket, "POST", body, cookie, cookieMsg)
        elif fileName == "/login.html":
            if cookie == True  and body != "" :
                # logout first to signup
                client_socket.send(b'HTTP/1.1 404 Not Found\r\n')
                client_socket.send(b'Content-Type: text/html\r\n\r\n')
                client_socket.send(b'<html><head></head><body><h1>logout first to signup</h1></body></html>\r\n')
            else :
                handle_signup(client_socket, body)
        elif fileName == "/board.html":
            handle_comment(client_socket, body, cookie, cookieMsg)
    
    elif method == "GET":
        if fileName == "/index.html":
            sendIndex(client_socket, "GET", "", cookie, cookieMsg)
        elif fileName == "/login.html":
            if cookie == True:
                # logout first
                client_socket.send(b'HTTP/1.1 404 Not Found\r\n')
                client_socket.send(b'Content-Type: text/html\r\n\r\n')
                client_socket.send(b'<html><head></head><body><h1>logout first to sign up or sign in</h1></body></html>\r\n')
            else :
                sendFile(client_socket, "/login.html", "html")
        elif fileName == "/board.html":
            sendBoard(client_socket, "GET", "", cookie, cookieMsg)
        elif fileName == "/logout.html":
            sendLogout(client_socket, cookieMsg)




def threadForReq(client_socket):
    try:
        # parse request
        message = client_socket.recv(4096).decode('utf-8')
        print(message)
        
        method = message.split()[0] # method
        fileName = message.split()[1] # file name
        if fileName == "/":
                fileName = "/index.html"
        fileType = fileName.split('.')[1] # file type
        
        if fileType != "html":
            sendFile(client_socket, fileName, fileType)
        else :
            body = unquote(unquote(message.split('\r\n\r\n')[1])) # form data
            cookie = False # cookie
            cookieMsg = ""
            
            if "Cookie" in message:
                cookie = True
                cookieMsg = message[message.find("Cookie: "):].split('\r\n')[0][8:]
                
            handleReq(client_socket, method, fileName, body, cookie, cookieMsg)
                    
    except IndexError:
        print("IndexError")
    except UnicodeDecodeError:
        print("UnicodeDecodeError")
        
    client_socket.close()



serverSocket = socket(AF_INET, SOCK_STREAM) # create server socket
serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1) # reuse the port
serverSocket.bind((HOST,PORT)) # bind port with server socket
serverSocket.listen(5) # listen

while True:
    print('Ready to serve for a new request...')
    connectionSocket, address = serverSocket.accept() # accept request
    print(str(address)+" connected")
    _thread.start_new_thread(threadForReq, (connectionSocket, ))
    
serverSocket.close()
sys.exit()
