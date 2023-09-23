package models

import (
	"errors"
	"time"
)

var ErrNoRecord = errors.New("models: подходящей записи не найдено")

type trunk struct {
	ID      int
	Title   string
	Content string
	Created time.Time
	Expires time.Time
}

/*
Обратите внимание, как названия полей структуры Snippet соответствуют полям в MySQL таблице snippets?
*/
