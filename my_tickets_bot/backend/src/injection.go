package main

import (
	"github.com/gin-gonic/gin"
	"log"
	"mytickets/src/handler"
	"mytickets/src/repository"
	"mytickets/src/service"
)

func inject(d *dataSources) (*gin.Engine, error) {
	log.Println("Injecting data sources")

	eventRepository := repository.NewEventRepository(d.DB)
	parserRepository := repository.NewPGEventRepository(d.DB)

	eventService := service.NewEventService(eventRepository)
	parserService := service.NewParserService(parserRepository)

	router := gin.Default()

	handler.NewHandler(&handler.Config{
		R:             router,
		EventService:  eventService,
		ParserService: parserService,
	})

	return router, nil
}
