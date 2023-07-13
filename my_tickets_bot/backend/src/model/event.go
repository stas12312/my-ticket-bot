package model

import (
	"time"
)

type Event struct {
	Id        string    `db:"id" json:"id,omitempty"`
	Name      string    `db:"name" json:"name,omitempty"`
	Time      time.Time `db:"time" json:"time"`
	Link      string    `db:"link" json:"link,omitempty"`
	UUID      string    `db:"uuid" json:"uuid,omitempty"`
	CreatedAt time.Time `db:"created_at" json:"created_at"`
	EndTime   time.Time `db:"end_time" json:"end_time"`
	UserId    int64     `db:"user_id" json:"user_id,omitempty"`
	Location  Location  `db:"location" json:"location"`
}
