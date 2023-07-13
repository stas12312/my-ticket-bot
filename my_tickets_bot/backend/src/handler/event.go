package handler

import (
	"fmt"
	"github.com/gin-gonic/gin"
	"log"
	"mytickets/src/apperrors"
	"mytickets/src/model"
	"mytickets/src/service/calendar"
	"net/http"
	"net/url"
	"strings"
	"time"
)

func (h *Handler) Calendar(c *gin.Context) {
	eventUUID := c.Param("eventUUID")

	event, err := h.EventService.Get(c, eventUUID)
	if err != nil {
		log.Println(err.Error())
		err := apperrors.NewNotFound("event", eventUUID)
		c.JSON(err.Status(), gin.H{
			"error": err,
		})
		return
	}

	body := CreateCalendarForEvent(event)
	filename := url.QueryEscape(event.Name)
	c.Writer.Header().Set("Content-Type", "text/calendar")
	c.Writer.Header().Set("Content-Disposition", fmt.Sprintf(`attachment; filename="%s.ics"`, filename))

	c.Writer.WriteHeader(http.StatusOK)
	_, err = c.Writer.WriteString(body)
	if err != nil {
		log.Println(err.Error())
		log.Println("Ошибка формирования ответа")
	}
}

func CreateCalendarForEvent(event *model.Event) string {
	e := calendar.NewEvent()
	e.AddDTStart(event.Time)
	if !event.EndTime.IsZero() {
		e.AddDTEnd(event.EndTime)
	}
	e.AddDTStamp(time.Now())
	e.AddSummary(event.Name)
	e.AddLocation(event.Location.Name)
	e.AddDescription(MakeDescription(event))

	c := calendar.NewCalendar()
	c.AddEvent(e)
	return c.ToString()

}

func MakeDescription(event *model.Event) string {
	var b strings.Builder
	b.WriteString("📍 " + MakeAddress(&event.Location))

	if event.Link != "" {
		b.WriteString("🔗 " + event.Link)
	}

	return b.String()
}

func MakeAddress(location *model.Location) string {
	return fmt.Sprintf("%s, %s", location.City.Name, location.Address)
}
