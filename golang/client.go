package main

import (
	"bufio"
	"fmt"
	"log"
	"net"
	"os"
)

func main() {
	serverAddr := "127.0.0.1:3001"	//address of server
	

	conn, err := net.Dial("tcp", serverAddr) //establish TCP connection using net.Dial
	if err != nil {
		log.Fatal("Connection error:", err)
	}

	defer conn.Close() //to make sure connection to TCP is closed afterwards, regardless of how program ends

	fmt.Println("Connected to server. Type messages to send:")

	go func() {	//start a goroutine, runs in parallel to handle incoming messages FROM the server.
		scanner := bufio.NewScanner(conn)	// wraps connection in a buffered scanner, line-by-line reading of server responses
		for scanner.Scan() {	// for each incoming message, we will do scan() which will read the message
			fmt.Println("Server response:", scanner.Text())	//text() extracts the received message as a string. we print it
		}
		if err := scanner.Err(); err != nil {	//any errors, we log
			log.Println("Error reading from server:", err)
		}
	}()

	scanner := bufio.NewScanner(os.Stdin)	//creates a reader for user input from the terminal (os.Stdin)

	for scanner.Scan(){		// scan() will read the message
		msg := scanner.Text()	//convert to string using Text()
		if msg == "exit"{	//if message is exit, we will break and exit program
			break
		}
		
		_, err := conn.Write([]byte(msg + "\n"))	//converts the input text to a byte slice and sends it to the server over the TCP connection
		if err != nil {
			log.Println("Error sending message:", err)
			break
		}
	}

	if err := scanner.Err(); err != nil {	//if we ever encounter any errors throughout process, we log it.
		log.Println("Error reading input:", err)
	}
	fmt.Println("Client exiting...")
}