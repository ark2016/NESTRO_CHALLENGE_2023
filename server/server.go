package main

import (
	"fmt"
	"net"
)

// требуется только ниже для обработки примера

/*
func main() {

	fmt.Println("Launching server...")

	// Устанавливаем прослушивание порта
	ln, _ := net.Listen("tcp", ":8081")

	// Открываем порт
	conn, _ := ln.Accept()

	// Запускаем цикл
	for {
		// Будем прослушивать все сообщения разделенные \n
		message, _ := bufio.NewReader(conn).ReadString('\n')
		// Распечатываем полученое сообщение
		if len(message) != 0 {
			fmt.Print("Message Received:", string(message))
			// Процесс выборки для полученной строки
			newmessage := strings.ToUpper(message)
			// Отправить новую строку обратно клиенту
			conn.Write([]byte(newmessage + "\n"))
		}
	}
}

*/

func main() {
	listener, _ := net.Listen("tcp", "127.0.0.1:8080") // открываем слушающий сокет
	for {
		conn, err := listener.Accept() // принимаем TCP-соединение от клиента и создаем новый сокет
		if err != nil {
			continue
		}
		go handleClient(conn) // обрабатываем запросы клиента в отдельной го-рутине
	}
}

func handleClient(conn net.Conn) {
	defer conn.Close() // закрываем сокет при выходе из функции

	buf := make([]byte, 32) // буфер для чтения клиентских данных
	for {
		conn.Write([]byte("Hello, what's your name?\n")) // пишем в сокет

		readLen, err := conn.Read(buf) // читаем из сокета
		if err != nil {
			fmt.Println(err)
			break
		}

		conn.Write(append([]byte("Goodbye, "), buf[:readLen]...)) // пишем в сокет
	}
}
