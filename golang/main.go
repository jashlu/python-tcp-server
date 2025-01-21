package main

import (
	"net"
	"fmt"
	"log"
)

type Server struct {
	listenAddr string
	ln net.Listener

	quitch chan struct{}
	msgch chan []byte
}

func NewServer(listenAddr string) *Server {
	return &Server{
		listenAddr: listenAddr,
		quitch: make(chan struct{}),
		msgch: make(chan []byte),
	}
}

func (s *Server) Start() error {
	ln, err := net.Listen("tcp", s.listenAddr)
	if err != nil {
		return err
	}
	defer ln.Close()
	s.ln = ln

	go s.acceptLoop()

	<-s.quitch				//wait until quitch returns stopped signal
	close(s.msgch)

	return nil
}

func (s *Server) acceptLoop() {
	for {
		conn, err := s.ln.Accept()
		if err != nil {
			fmt.Println("accept error:", err)
			continue
		} 

		fmt.Println("new connection to the server:", conn.RemoteAddr())
		go s.readLoop(conn)
	}
}

func (s *Server) readLoop(conn net.Conn){
	defer conn.Close()
	
	buf := make([]byte, 2048)
	for {
		n, err := conn.Read(buf)
		if err != nil {
			fmt.Println("read error: ", err)
			continue
		}

		msg := buf[:n]
		s.msgch <- msg		//send msg to the main channel
	}	
}


func main() {
	server := NewServer(":3001")
	
	//Go routine to process messages recevied by the server.
	go func() {
		for msg := range server.msgch {
			fmt.Println("Received message from connection:", string(msg))
		}
	}()

	log.Fatal(server.Start())
}