package model

type City struct {
	Id        int64  `db:"id" json:"id,omitempty"`
	Name      string `db:"name" json:"name,omitempty"`
	Timezone  string `db:"timezone" json:"timezone,omitempty"`
	IsDeleted bool   `db:"is_deleted" json:"is_deleted,omitempty"`
}
