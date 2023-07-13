package service

import (
	"context"
	"mytickets/src/model"
)

type ParserService struct {
	ParserRepository model.ParserRepository
}

func NewParserService(parserRepository model.ParserRepository) model.ParserService {
	return &ParserService{
		ParserRepository: parserRepository,
	}
}

func (s *ParserService) Get(ctx context.Context, id int64) (*model.Parser, error) {
	parser, err := s.ParserRepository.GetById(ctx, id)
	return parser, err
}

func (s *ParserService) List(ctx context.Context) ([]model.Parser, error) {
	parsers, err := s.ParserRepository.ListAll(ctx)
	return parsers, err
}
