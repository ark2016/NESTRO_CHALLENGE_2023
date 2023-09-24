package models

import (
	"errors"
	"time"
)

var ErrNoRecord = errors.New("models: подходящей записи не найдено")

type trunk struct {
	ID                  int
	Model               string
	ParamCharge         int
	ParamQn             float64
	ParamQg             float64
	ParamQv             float64
	P                   float64
	T                   float64
	ParamFlowRegime     string
	ParamFacticVelocity int
	ParamCriticVelocity int
	ParamCrash          int
	ParamLifetime       int
	ResidualResource    int
	Created             time.Time
}

/*
Обратите внимание, как названия полей структуры Snippet соответствуют полям в MySQL таблице snippets?
*/
