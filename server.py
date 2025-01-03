import socket

#create a socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM);

#port
port = 5001

""" binds the socket to a specific address """
s.bind(("", port))

""" tells operating system to start listening for connections on the socket """
s.listen(5)

while(True):
    #accept a new client connection (and waits for next connection)
    c, a = s.accept() 
    print("Received message from " + str(a))
    #send data to client
    c.send(b"Hello in server !!")

    #close client connection
    c.close()