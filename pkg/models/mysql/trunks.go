package mysql

import (
	"database/sql"
	"errors"
	"nestroh/pkg/models"
)

/*
Обратите внимание, как названия полей структуры Snippet соответствуют полям в MySQL таблице snippets?
*/

// SnippetModel - Определяем тип который обертывает пул подключения sql.DB
type TrunkModel struct {
	DB *sql.DB
}

// Insert - Метод для создания новой заметки в базе дынных.
func (m *TrunkModel) Insert(Model string, ParamCharge int, ParamQn float64,
	ParamQg float64,
	ParamQv float64,
	P float64,
	T float64,
	ParamFlowRegime string,
	ParamFacticVelocity int,
	ParamCriticVelocity int,
	ParamCrash int,
	ParamLifetime int,
	ResidualResource int) (int, error) {
	// Ниже будет SQL запрос, который мы хотим выполнить. Мы разделили его на две строки
	// для удобства чтения (поэтому он окружен обратными кавычками
	// вместо обычных двойных кавычек).
	stmt := `INSERT INTO trunks (Model, ParamCharge, ParamQn, ParamQg, ParamQv,
P                   ,
T                   ,
ParamFlowRegime     ,
ParamFacticVelocity ,
ParamCriticVelocity ,
ParamCrash          ,
ParamLifetime       ,
ResidualResource, created)
    VALUES(?, ?, ?, ?, ?,
?,
?,
?,
?,
?,
?,
?,
?, UTC_TIMESTAMP())`

	// Используем метод Exec() из встроенного пула подключений для выполнения
	// запроса. Первый параметр это сам SQL запрос, за которым следует
	// заголовок заметки, содержимое и срока жизни заметки. Этот
	// метод возвращает объект sql.Result, который содержит некоторые основные
	// данные о том, что произошло после выполнении запроса.
	result, err := m.DB.Exec(stmt, Model, ParamCharge, ParamQn,
		ParamQg,
		ParamQv,
		P,
		T,
		ParamFlowRegime,
		ParamFacticVelocity,
		ParamCriticVelocity,
		ParamCrash,
		ParamLifetime,
		ResidualResource)
	if err != nil {
		return 0, err
	}

	// Используем метод LastInsertId(), чтобы получить последний ID
	// созданной записи из таблицу snippets.
	id, err := result.LastInsertId()
	if err != nil {
		return 0, err
	}

	// Возвращаемый ID имеет тип int64, поэтому мы конвертируем его в тип int
	// перед возвратом из метода.
	return int(id), nil
}

// Get - Метод для возвращения данных заметки по её идентификатору ID.
func (m *TrunkModel) Get(id int) (*models.Trunk, error) {
	// SQL запрос для получения данных одной записи.
	stmt := `SELECT id, Model, ParamCharge, ParamQn,
		ParamQg,
		ParamQv,
		P,
		T,
		ParamFlowRegime,
		ParamFacticVelocity,
		ParamCriticVelocity,
		ParamCrash,
		ParamLifetime,
		ResidualResource, created FROM trunks
    WHERE id = ?`

	// Используем метод QueryRow() для выполнения SQL запроса,
	// передавая ненадежную переменную id в качестве значения для плейсхолдера
	// Возвращается указатель на объект sql.Row, который содержит данные записи.
	row := m.DB.QueryRow(stmt, id)

	// Инициализируем указатель на новую структуру Snippet.
	s := &models.Trunk{}

	// Используйте row.Scan(), чтобы скопировать значения из каждого поля от sql.Row в
	// соответствующее поле в структуре Snippet. Обратите внимание, что аргументы
	// для row.Scan - это указатели на место, куда требуется скопировать данные
	// и количество аргументов должно быть точно таким же, как количество
	// столбцов в таблице базы данных.
	err := row.Scan(&s.ID, &s.Model, &s.ParamCharge, &s.ParamQn,
		&s.ParamQg,
		&s.ParamQv,
		&s.P,
		&s.T,
		&s.ParamFlowRegime,
		&s.ParamFacticVelocity,
		&s.ParamCriticVelocity,
		&s.ParamCrash,
		&s.ParamLifetime,
		&s.ResidualResource, &s.Created)
	if err != nil {
		// Специально для этого случая, мы проверим при помощи функции errors.Is()
		// если запрос был выполнен с ошибкой. Если ошибка обнаружена, то
		// возвращаем нашу ошибку из модели models.ErrNoRecord.
		if errors.Is(err, sql.ErrNoRows) {
			return nil, models.ErrNoRecord
		} else {
			return nil, err
		}
	}

	// Если все хорошо, возвращается объект Snippet.
	return s, nil
}

/*
Под капотом метода rows.Scan(), драйвер базы данных автоматически преобразует MySQL типы в типы языка программирования Go:

CHAR, VARCHAR и TEXT соответствуют типу string;
BOOLEAN соответствует bool;
INT соответствует int;
BIGINT соответствует int64;
DECIMAL и NUMERIC соответствуют float;
TIME, DATE и TIMESTAMP соответствуют time.Time.
*/
