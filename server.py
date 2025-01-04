import socket

# create a socket
# specifies the address, AF_INET
# specifies the socket type, TCP
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM);

#port
port = 5001

""" binds the socket to a specific address """
# associate socket with specific port, 5001 in this case
# empty string means server will listen on all available interfaces
s.bind(("", port))

""" tells operating system to start listening for connections on the socket """
# server enters listening state, waiting for incoming client connections
# 5 represents max number of queued connection requests before refusing new ones
s.listen(5)

print("Server set up. Now listening for requests...")

while(True):
    #accept a new client connection (and waits for next connection)
    #c is new socket object for communication
    #a is address of the connected client (IP and port)
    c, a = s.accept() 

    while True:
        # Receive data from the client
        data = c.recv(1024).decode()
        if not data:  # If no data, client has closed the connection
            print(f"Connection with {a} closed.")
            break
        print(f"Client {a} says: {data}")

        # Send a response to the client
        message = f"Received your message"
        c.send(message.encode())

    # Close client connection
    c.close()