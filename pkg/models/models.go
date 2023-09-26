package models

import (
	"errors"
	"time"
)

var ErrNoRecord = errors.New("models: подходящей записи не найдено")

type Trunk struct {
	ID                  int
	Model               string
	ParamCharge         float64
	ParamQn             float64
	ParamQg             string
	ParamQv             float64
	P                   float64
	T                   float64
	ParamFlowRegime     string
	ParamFacticVelocity float64
	ParamCriticVelocity float64
	ParamCrash          float64
	ParamLifetime       float64
	ResidualResource    float64
	Created             time.Time
}

/*
Обратите внимание, как названия полей структуры Snippet соответствуют полям в MySQL таблице snippets?
*/
