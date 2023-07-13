package model

import "time"

type User struct {
	Id        int64     `db:"id" json:"id,omitempty"`
	Username  string    `json:"username,omitempty"`
	CreatedAt time.Time `json:"created_at"`
	FirstName string    `json:"first_name,omitempty"`
	LastName  string    `json:"last_name,omitempty"`
}
