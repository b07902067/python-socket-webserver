from socket import *
import time
import sys
import pickle
import json
from urllib.parse import unquote
import re
import numpy as np
import datetime

file_type_dict = {"html" : "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n", "css" : "HTTP/1.1 200 OK\r\nContent-Type: text/css\r\n\r\n" , "js" : "HTTP/1.1 200 OK\r\nContent-Type: text/javascript\r\n\r\n"}


# for css, js, login.html
def sendFile(client_socket, file_name, file_type):
    try:
        f = open(file_name[1:])
        outputdata=f.readlines()
        client_socket.send(file_type_dict[file_type].encode())
        for i in range(0, len(outputdata)):
            client_socket.send(outputdata[i].encode())
        client_socket.send("\r\n".encode())
            
    except IndexError:
        print("IndexError")
        
        # file not found
    except FileNotFoundError:
        print("FileNotFoundError")
        client_socket.send(b'HTTP/1.1 404 Not Found\r\n')
        client_socket.send(b'Content-Type: text/html\r\n\r\n')
        client_socket.send(b'<html><head></head><body><h1>404 Not found</h1></body></html>\r\n')



def sendIndex(client_socket, method, body, cookie, cookieMsg):
    # <li class="nav-item"><a class="nav-link js-scroll-trigger" href="/login.html">login</a></li>
    try:
        f_head = open("index_head")
        f_tail = open("index_tail")
        head_data = f_head.readlines()
        tail_data = f_tail.readlines()
        with open("pass_sid.pickle", 'rb') as handle:
            pass_sid_Dict = pickle.load(handle)
        with open("user.pickle", 'rb') as handle:
            userDict = pickle.load(handle)
        
        if method == "GET" :
            client_socket.send(file_type_dict["html"].encode())
            if cookie == False:
                for i in range(0, len(head_data)):
                    client_socket.send(head_data[i].encode())
                client_socket.send('<li class="nav-item"><a class="nav-link js-scroll-trigger" href="/login.html">login</a></li>'.encode())
                for i in range(0, len(tail_data)):
                    client_socket.send(tail_data[i].encode())
            elif cookie == True:
                # deal with cookie: sid=
                sid = cookieMsg[cookieMsg.find("sid=")+4:]
                sid = sid.strip().split(";")[0]
                # get username
                userName = userDict[sid]
                for i in range(0, len(head_data)):
                    client_socket.send(head_data[i].encode())
                client_socket.send('<li class="nav-item"><a class="nav-link js-scroll-trigger" href="#">'.encode())
                client_socket.send(userName.encode())
                client_socket.send('</a></li><li class="nav-item"><a class="nav-link js-scroll-trigger" href="/logout.html">logout</a></li>'.encode())
                for i in range(0, len(tail_data)):
                    client_socket.send(tail_data[i].encode())
        elif method == "POST" :
            if cookie == False:
                data_list = re.split(r"[&, =]", body)
                name = data_list[1]
                passwd = data_list[3]
                if name in pass_sid_Dict and pass_sid_Dict[name][0] == passwd:
                    client_socket.send("HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nSet-Cookie: sid=".encode())
                    client_socket.send(pass_sid_Dict[name][1].encode())
                    client_socket.send("; Expires=".encode())
                    time_str = datetime.datetime.now()+ datetime.timedelta(days=1)
                    time_str = time_str.strftime("%a, %d %b %Y %H:%M:%S GMT+8").encode()
                    client_socket.send(time_str)
                    client_socket.send(";\r\n\r\n".encode())
                    for i in range(0, len(head_data)):
                        client_socket.send(head_data[i].encode())
                    client_socket.send('<li class="nav-item"><a class="nav-link js-scroll-trigger" href="#">'.encode())
                    client_socket.send(name.encode())
                    client_socket.send('</a></li><li class="nav-item"><a class="nav-link js-scroll-trigger" href="/logout.html">logout</a></li>'.encode())
                    for i in range(0, len(tail_data)):
                        client_socket.send(tail_data[i].encode())
                else :
                    # invalid username or password
                    client_socket.send(b'HTTP/1.1 404 Not Found\r\n')
                    client_socket.send(b'Content-Type: text/html\r\n\r\n')
                    client_socket.send(b'<html><head></head><body><h1>invalid username or password</h1></body></html>\r\n')
    except IndexError:
        print("IndexError")
        
        # file not found
    except FileNotFoundError:
        print("FileNotFoundError")
        client_socket.send(b'HTTP/1.1 404 Not Found\r\n')
        client_socket.send(b'Content-Type: text/html\r\n\r\n')
        client_socket.send(b'<html><head></head><body><h1>404 Not found</h1></body></html>\r\n')
                
                
                
                
            
    
def sendBoard(client_socket, method, userName, cookie, cookieMsg):
    # <li class="right"><a href="#">username</a></li>
    # <li class="right"><a href="/logout.html">logout</a></li>
    try:
        with open("board.pickle", 'rb') as handle:
            msg_dict = pickle.load(handle)
        empty = not bool(msg_dict)
        client_socket.send(file_type_dict["html"].encode())
        
        f_head = open("board_head")
        f_tail = open("board_tail")
        head_data = f_head.readlines()
        tail_data = f_tail.readlines()
                
        for i in range(0, len(head_data)):
            client_socket.send(head_data[i].encode())
        if cookie == True:
            name = ""
            if method == "GET":
                with open("user.pickle", 'rb') as handle:
                    userDict = pickle.load(handle)
                sid = cookieMsg[cookieMsg.find("sid=")+4:]
                sid = sid.strip().split(";")[0]
                # get username
                name = userDict[sid]
            elif method == "POST":
                name = userName
            client_socket.send('<li class="right"><a href="#">'.encode())
            client_socket.send(name.encode())
            client_socket.send('</a></li><li class="right"><a href="/logout.html">logout</a></li>'.encode())
        for i in range(0, len(tail_data)):
            client_socket.send(tail_data[i].encode())
        
        tmp_dict = {}
        if empty == False:
            comments = 0
            overflow = False
            for key in sorted(msg_dict, reverse=True):
                comments += 1
                tmp_dict[key] = msg_dict[key]
                client_socket.send(b'<div class="post"><h3 class="title">')
                client_socket.send(msg_dict[key][0].encode())
                client_socket.send(b'</h3><p class="meta"><span class="date">')
                client_socket.send(key.encode())
                client_socket.send(b'</span></p><div class="entry"><h4>')
                client_socket.send(msg_dict[key][1].encode())
                client_socket.send(b'</h4></div></div>')
                if comments == 100:
                    overflow = True
                    break
        client_socket.send(b'</div></div></body></html>\r\n')
        if overflow == True:
            with open("board.pickle", 'wb') as handle:
                pickle.dump(tmp_dict, handle)
    except IndexError:
        print("IndexError")
        
        # file not found
    except FileNotFoundError:
        print("FileNotFoundError")
        client_socket.send(b'HTTP/1.1 404 Not Found\r\n')
        client_socket.send(b'Content-Type: text/html\r\n\r\n')
        client_socket.send(b'<html><head></head><body><h1>404 Not found</h1></body></html>\r\n')


def handle_comment(client_socket, data, cookie, cookieMsg):
    try:
        comment = data.replace("+" , " ")[2:]
        with open("board.pickle", 'rb') as handle:
            msg_dict = pickle.load(handle)
        with open("user.pickle", 'rb') as handle:
            userDict = pickle.load(handle)
        time_now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        name = "Guest"
        if cookie == True:
            sid = cookieMsg[cookieMsg.find("sid=")+4:]
            sid = sid.strip().split(";")[0]
            # get username
            name = userDict[sid]
        
        msg_dict[time_now] = [name , comment]
        with open("board.pickle", 'wb') as handle:
            pickle.dump(msg_dict, handle)
        sendBoard(client_socket, "POST", name, cookie, cookieMsg)
    except IndexError:
        print("IndexError")
        
        # file not found
    except FileNotFoundError:
        print("FileNotFoundError")
        client_socket.send(b'HTTP/1.1 404 Not Found\r\n')
        client_socket.send(b'Content-Type: text/html\r\n\r\n')
        client_socket.send(b'<html><head></head><body><h1>404 Not found</h1></body></html>\r\n')
        
    


#fullname=aaa&password=bbb&confirmpassword=ccc
def handle_signup(client_socket, data):
    data_list = re.split(r"[&, =]", data)
    account = data_list[1]
    passwd = data_list[3]
    confirmpasswd = data_list[5]
    if passwd != confirmpasswd :
        client_socket.send(b'HTTP/1.1 404 Not Found\r\n')
        client_socket.send(b'Content-Type: text/html\r\n\r\n')
        client_socket.send(b'<html><head></head><body><h1>password is not the same</h1></body></html>\r\n')
    else :
        with open("pass_sid.pickle", 'rb') as handle:
            pass_sid_Dict = pickle.load(handle)
        with open("user.pickle", 'rb') as handle:
            userDict = pickle.load(handle)
        if account in pass_sid_Dict:
            client_socket.send(b'HTTP/1.1 404 Not Found\r\n')
            client_socket.send(b'Content-Type: text/html\r\n\r\n')
            client_socket.send(b'<html><head></head><body><h1>username already exist</h1></body></html>\r\n')
        else:
            sid = str(np.array([13*ord(c) for c in account]).sum()%100000 + 10000)
            pass_sid_Dict[account] = [passwd, sid]
            userDict[sid] = account
            with open("pass_sid.pickle", 'wb') as handle:
                pickle.dump(pass_sid_Dict, handle)
            with open("user.pickle", 'wb') as handle:
                pickle.dump(userDict, handle)
            sendFile(client_socket, "/login.html", "html")


def sendLogout(client_socket, cookieMsg):
    f_head = open("index_head")
    f_tail = open("index_tail")
    head_data = f_head.readlines()
    tail_data = f_tail.readlines()
    sid = cookieMsg[cookieMsg.find("sid=")+4:]
    sid = sid.strip().split(";")[0]
    
    client_socket.send("HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nSet-Cookie: sid=".encode())
    client_socket.send(sid.encode())
    client_socket.send("; Expires=".encode())
    time_str = datetime.datetime.now()+ datetime.timedelta(days=-10)
    time_str = time_str.strftime("%a, %d %b %Y %H:%M:%S GMT+8").encode()
    client_socket.send(time_str)
    client_socket.send(";\r\n\r\n".encode())
    
    for i in range(0, len(head_data)):
        client_socket.send(head_data[i].encode())
    client_socket.send('<li class="nav-item"><a class="nav-link js-scroll-trigger" href="/login.html">login</a></li>'.encode())
    for i in range(0, len(tail_data)):
        client_socket.send(tail_data[i].encode())
