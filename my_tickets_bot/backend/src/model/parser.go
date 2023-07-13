package model

type ParserEvent struct {
	Name     string `json:"name,omitempty"`
	Url      string `json:"url,omitempty"`
	Datetime string `json:"datetime,omitempty"`
}

type Parser struct {
	Id          int64         `db:"id" json:"id,omitempty"`
	Name        string        `db:"name" json:"name,omitempty"`
	Url         string        `db:"url" json:"url,omitempty"`
	EventsCount int           `db:"events_count" json:"events_count,omitempty"`
	Timezone    string        `db:"timezone" json:"timezone,omitempty"`
	Timestamp   string        `db:"timestamp" json:"timestamp,omitempty"`
	Events      []ParserEvent `json:"events"`
}
