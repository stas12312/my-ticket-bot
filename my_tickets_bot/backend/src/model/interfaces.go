package model

import "context"

type EventService interface {
	Get(ctx context.Context, uuid string) (*Event, error)
}

type EventRepository interface {
	GetByUUID(ctx context.Context, uuid string) (*Event, error)
}

type ParserService interface {
	Get(ctx context.Context, id int64) (*Parser, error)
	List(ctx context.Context) ([]Parser, error)
}

type ParserRepository interface {
	GetById(ctx context.Context, id int64) (*Parser, error)
	ListAll(ctx context.Context) ([]Parser, error)
}
