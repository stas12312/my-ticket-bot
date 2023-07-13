package handler

import (
	"github.com/gin-gonic/gin"
	"mytickets/src/model"
)

type Handler struct {
	EventService  model.EventService
	ParserService model.ParserService
}
type Config struct {
	R             *gin.Engine
	EventService  model.EventService
	ParserService model.ParserService
}

func NewHandler(c *Config) {
	h := &Handler{
		EventService:  c.EventService,
		ParserService: c.ParserService,
	}
	api := c.R.Group("api")

	eventGroup := c.R.Group("/events")
	eventGroup.GET("/:eventUUID/calendar-ics", h.Calendar)

	parserGroup := api.Group("/parsers")
	parserGroup.GET("/", h.ParserList)
	parserGroup.GET("/:parserId", h.GetParser)
}
