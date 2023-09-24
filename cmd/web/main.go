package main

import (
	"database/sql"
	"flag"
	_ "github.com/go-sql-driver/mysql" // Новый импорт
	"log"
	"nestroh/pkg/models/mysql"
	"net/http"
	"os"
)

// web сервер запускается из файла server.go

type application struct {
	errorLog *log.Logger
	infoLog  *log.Logger
	trunks   *mysql.TrunkModel
}

func main() {
	addr := flag.String("addr", ":4000", "Сетевой адрес веб-сервера")
	// Определение нового флага из командной строки для настройки MySQL подключения.
	dsn := flag.String("dsn", "web:web00top@/hack?parseTime=true", "Название MySQL источника данных")
	flag.Parse()

	infoLog := log.New(os.Stdout, "INFO\t", log.Ldate|log.Ltime)
	errorLog := log.New(os.Stderr, "ERROR\t", log.Ldate|log.Ltime|log.Lshortfile)

	// Чтобы функция main() была более компактной, мы поместили код для создания
	// пула соединений в отдельную функцию openDB(). Мы передаем в нее полученный
	// источник данных (DSN) из флага командной строки.
	db, err := openDB(*dsn)
	if err != nil {
		errorLog.Fatal(err)
	}

	// Мы также откладываем вызов db.Close(), чтобы пул соединений был закрыт
	// до выхода из функции main().
	// Подробнее про defer: https://golangs.org/errors#defer
	defer db.Close()

	app := &application{
		errorLog: errorLog,
		infoLog:  infoLog,
		trunks:   &mysql.TrunkModel{DB: db},
	}

	srv := &http.Server{
		Addr:     *addr,
		ErrorLog: errorLog,
		Handler:  app.routes(),
	}

	infoLog.Printf("Запуск сервера на %s", *addr)
	// Поскольку переменная `err` уже объявлена в приведенном выше коде, нужно
	// использовать оператор присваивания =
	// вместо оператора := (объявить и присвоить)
	err = srv.ListenAndServe()
	errorLog.Fatal(err)
}

// Функция openDB() обертывает sql.Open() и возвращает пул соединений sql.DB
// для заданной строки подключения (DSN).
func openDB(dsn string) (*sql.DB, error) {
	db, err := sql.Open("mysql", dsn)
	if err != nil {
		return nil, err
	}
	if err = db.Ping(); err != nil {
		return nil, err
	}
	// Устанавливаем максимальное количество одновременно открытых (простаивающих + используемых) соединений.
	// Указание этого значения меньше или равного 0 будет означать, что ограничений нет. Если максимальное
	// количество открытых подключений достигнуто и все они используются, но нам требуется новое подключение,
	// тогда Go будет ждать, пока одно из подключений не освободится. С точки зрения
	// пользователя это означает, что HTTP запрос будет загружаться до тех пор, пока
	// соединение с базой данных не станет доступным. По сути, у пользователя зависнет сайт.
	db.SetMaxOpenConns(100)

	// Устанавливаем максимальное количество неактивных соединений в пуле. Указание этого
	// значения меньше или равного 0 будет означать, что неактивные соединения не будут создаваться.
	// Каждый запрос создаст новое подключение и сразу начнет с ней работу.
	db.SetMaxIdleConns(5)
	return db, nil
}

/*

Если вы не будете использовать плейсхолдеры, то вы рискуете оставить уязвимость в виде SQL-инъекции.

установка драйвера для базы
go get github.com/go-sql-driver/mysql

обновление пакета
go get -u github.com/foo/bar

далить пакет из Golang?
$ go get github.com/foo/bar@none



GRANT SELECT, INSERT, UPDATE ON hack.* TO 'web'@'localhost';

-- Важно: Не забудьте заменить 'pass' на свой пароль, иначе это и будет паролем.
ALTER USER 'web'@'localhost' IDENTIFIED BY 'web00top';


*/
