package repository

import (
	"context"
	"github.com/goccy/go-json"
	"github.com/jmoiron/sqlx"
	"mytickets/src/model"
	"mytickets/src/repository/query"
)

type PGParserRepository struct {
	DB *sqlx.DB
}

type PublicKey struct {
	Name  string
	Price string
}

func (p *PGParserRepository) GetById(ctx context.Context, id int64) (*model.Parser, error) {
	row := p.DB.QueryRow(query.GetParser, id)
	var parserId int64
	var name, url, timezone, timestamp, rawEvents string
	var eventCounts int

	err := row.Scan(&parserId, &name, &url, &eventCounts, &timezone, &timestamp, &rawEvents)
	if err != nil {
		return nil, err
	}

	events := make([]model.ParserEvent, 0)

	err = json.Unmarshal([]byte(rawEvents), &events)
	if err != nil {
		return nil, err
	}
	parser := &model.Parser{
		Id:          id,
		Name:        name,
		Url:         url,
		EventsCount: eventCounts,
		Timestamp:   timestamp,
		Timezone:    timezone,
		Events:      events,
	}

	return parser, err
}

func (p *PGParserRepository) ListAll(ctx context.Context) ([]model.Parser, error) {
	var parsers []model.Parser
	err := p.DB.Select(&parsers, query.ListParser)

	return parsers, err
}

func NewPGEventRepository(db *sqlx.DB) model.ParserRepository {
	return &PGParserRepository{
		DB: db,
	}
}
