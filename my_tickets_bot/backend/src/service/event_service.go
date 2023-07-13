package service

import (
	"context"
	"mytickets/src/model"
)

type EventService struct {
	EventRepository model.EventRepository
}

func (s *EventService) Get(ctx context.Context, uuid string) (*model.Event, error) {
	u, err := s.EventRepository.GetByUUID(ctx, uuid)
	return u, err
}

func NewEventService(eventRepository model.EventRepository) model.EventService {
	return &EventService{
		EventRepository: eventRepository,
	}
}
