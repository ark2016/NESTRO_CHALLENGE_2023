package main

import (
	"./web"
	"fmt"
	"net"
	"os"
	"strings"
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
	go web.Web()                                       // запуск веб-сервера на порте 4000
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
	web_id := -1
	for {
		//conn.Write([]byte("Do you want start web-server?\n")) // пишем в сокет

		readLen, err := conn.Read(buf) // читаем из сокета
		message := string(buf[:readLen])
		message = strings.TrimSpace(message)
		fmt.Println(message)
		if message == "start" && web_id == -1 {
			go web.Web()
			fmt.Println("Сервер начал работу")
			conn.Write(append([]byte("Сервер начал работу"))) // пишем в сокет
			web_id = web.Print_thread_id()
		} else if message == "stop" {
			process := os.Process{Pid: web_id}
			process.Kill()
			fmt.Println("Сервер остановлен")
			conn.Write(append([]byte("Сервер остановлен"))) // пишем в сокет
		} else {
			fmt.Println("Сервер не начал работу")
			conn.Write(append([]byte("Сервер не начал работу"))) // пишем в сокет
		}
		if err != nil {
			fmt.Println(err)
			break
		}

		//conn.Write(append([]byte("Goodbye, "), buf[:readLen]...)) // пишем в сокет
	}
}

func print_thread_id1() int {
	tid := os.Getpid()
	fmt.Printf("Thread ID: %v\n", tid)
	return tid
}
