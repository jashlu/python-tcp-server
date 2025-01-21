import socket
import click

#Connect
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
port = 5001
client_socket.connect(("localhost", port))
print(f"Conencted to server at localhost:{port}")

#Have client login

name = click.prompt("Please enter your name", type=str)

#Send message to server
message = f"Hello, server! This is the client, {name}"
client_socket.send(message.encode())

#Receive initial response
response = client_socket.recv(1024).decode()
print(f"Server: {response}")


while True:

    send_message = click.prompt(
                    "Would you like to send a message?",
                    show_choices=True,
                    type=click.Choice(["y", "n"], case_sensitive=False),
                )


    if send_message == "y":
        client_message = click.prompt("Enter your message", type=str)

        #Send message to server
        client_socket.send(client_message.encode())

        #Receive initial response
        response = client_socket.recv(1024).decode()
        print(f"Server: {response}")


    else:
        client_socket.close()
        break

print("Finished.")