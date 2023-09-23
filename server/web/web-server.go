package web

import (
	"flag"
	"fmt"
	"log"
	"net/http"
	"os"
	"syscall"
)

// web сервер запускается из файла server.go

func Web() {
	Print_thread_id()
	addr := flag.String("addr", ":4001", "Сетевой адрес веб-сервера")
	flag.Parse()

	// Используйте log.New() для создания логгера для записи информационных сообщений. Для этого нужно
	// три параметра: место назначения для записи логов (os.Stdout), строка
	// с префиксом сообщения (INFO или ERROR) и флаги, указывающие, какая
	// дополнительная информация будет добавлена. Обратите внимание, что флаги
	// соединяются с помощью оператора OR |.
	infoLog := log.New(os.Stdout, "INFO\t", log.Ldate|log.Ltime)

	// Создаем логгер для записи сообщений об ошибках таким же образом, но используем stderr как
	// место для записи и используем флаг log.Lshortfile для включения в лог
	// названия файла и номера строки где обнаружилась ошибка.
	errorLog := log.New(os.Stderr, "ERROR\t", log.Ldate|log.Ltime|log.Lshortfile)

	mux := http.NewServeMux()
	mux.HandleFunc("/", home)

	// Применяем созданные логгеры к нашему приложению.
	infoLog.Printf("Запуск сервера на %s", *addr)
	err := http.ListenAndServe(*addr, mux)
	errorLog.Fatal(err)
}

func Print_thread_id() int {
	tid := syscall.Getgid()
	fmt.Printf("Thread ID: %v\n", tid)
	return tid
}
