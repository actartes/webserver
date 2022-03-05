#
# Simple Webserver
#
import socket
import configparser


config = configparser.ConfigParser()
config.read("config.ini")

DEBUG_MODE = config["Server"]["DEBUG_MODE"]
TIMEOUT = config.getint("Server", "TIMEOUT")
HOST = config["Server"]["HOST"]
PORT = config.getint("Server", "PORT")


serv_addr = (HOST, PORT)

# Line below is for Windows / Python >3.10
#s = socket.create_server(serv_addr, family=socket.AF_INET)

#TODO: cycle socket creating
while True:
    s = socket.socket(socket.AF_INET)
    s.bind(serv_addr)
    # Later uncomment it
    # s.settimeout(TIMEOUT)

    # Tell us a little bit more about created listening socket
    if DEBUG_MODE == True:
        print("SOCKET: {}".format(s))

    s.listen(1)
    client_conn, client_addr = s.accept()

    # Tell us about requests that we got
    if DEBUG_MODE == True:
        print("CLIENT CONNECTION: {}".format(client_conn), "\f\n"
              "CLIENT ADDRESS: {}".format(client_addr))

    while True:
        data = client_conn.recv(1024)
    
        # Print each request
        if DEBUG_MODE == True:
            print(data.decode())
    
        # End of the first request from browser.
        # Here we need to stop listening and send something.
        if data[-4:] == b'\r\n\r\n':
            break

    with open("index.html", "r") as f:
        response_body = f.read()
        response_body_raw = str(response_body + "\n").encode("utf-8")
    
        if DEBUG_MODE == True:
            print(response_body)
        
    
    #TODO: define response headers in python structure
    response_headers = "Content-Type: text/html; charset=utf-8\nContent-Length: {}\nConnection: close".format(str(len(response_body_raw)))
    response_headers_raw = response_headers.encode()
    
    client_conn.send("HTTP/1.1 200 OK\n".encode())
    client_conn.send(response_headers_raw)
    client_conn.send("\n\n".encode())
    client_conn.send(response_body_raw)
    client_conn.close()
    s.close()