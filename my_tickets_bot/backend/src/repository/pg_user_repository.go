package repository

import (
	"context"
	"errors"
	"github.com/jackskj/carta"
	"github.com/jmoiron/sqlx"
	"mytickets/src/model"
	"mytickets/src/repository/query"
)

type PGEventRepository struct {
	DB *sqlx.DB
}

func NewEventRepository(db *sqlx.DB) model.EventRepository {
	return &PGEventRepository{
		DB: db,
	}
}

func (r *PGEventRepository) GetByUUID(ctx context.Context, uuid string) (*model.Event, error) {
	var events []model.Event

	rows, err := r.DB.Query(query.GetEventQuery, uuid)
	if err != nil {
		return nil, err
	}

	carta.Map(rows, &events)
	if len(events) < 1 {
		return nil, errors.New("not found")
	}
	return &events[0], nil
}
