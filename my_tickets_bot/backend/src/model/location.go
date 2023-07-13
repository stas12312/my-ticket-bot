package model

type Location struct {
	Id      int64  `db:"id" json:"id,omitempty"`
	Name    string `db:"name" json:"name,omitempty"`
	Address string `db:"address" json:"address,omitempty"`
	Url     string `db:"url" json:"url,omitempty"`
	City    City   `db:"city" json:"city"`
}
