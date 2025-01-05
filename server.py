import socket
import threading



# function to handle communication with a single client

def handle_client(client_socket, client_address):
    print(f"Connection established with {client_address}")

    while True:
        # receive data from the client
        # 1024 represents max bytes (1kb) that can be read from the socket at once
        data = client_socket.recv(1024).decode()
        # if no data, close.
        if not data:
            print(f"Connection with {client_address} closed.")
            break
        print(f"Client {client_address} says: {data}")

        # Send a response to the client
        message = f"Received your message"
        client_socket.send(message.encode())
    # close the client connection
    client_socket.close()



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
    # accept a new client connection (and waits for next connection)
    # c is new socket object for communication
    # a is address of the connected client (IP and port)
    client_socket, client_address = s.accept() 

    # create a new thread that will ahdnle the client
    # this allows server to handle multiple clients at once
    client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
    client_thread.start()