package calendar

import (
	"fmt"
	"strings"
	"time"
)

type Event struct {
	components map[string]string
}

func NewEvent() Event {
	return Event{
		components: map[string]string{},
	}
}

// AddComponent добавление компонента в событие календаря
func (event *Event) AddComponent(name string, value string) {
	event.components[name] = value
}

func (event *Event) AddTime(name string, value time.Time) {
	event.components[name] = value.Format("20060102T150405")
}

func (event *Event) AddText(name string, value string) {
	event.AddComponent(name, EscapeString(value))
}

func (event *Event) AddDTStart(dtStart time.Time) {
	event.AddTime(DTSTART, dtStart)
}

func (event *Event) AddDTEnd(dtEnd time.Time) {
	event.AddTime(DTEND, dtEnd)
}

func (event *Event) AddDTStamp(dtTime time.Time) {
	event.AddTime(DTSTAMP, dtTime)
}

func (event *Event) AddSummary(summary string) {
	event.AddText(SUMMARY, summary)
}

func (event *Event) AddLocation(location string) {
	event.AddText(LOCATION, location)
}

func (event *Event) AddDescription(description string) {
	event.AddText(DESCRIPTION, description)
}

// ToString  сериализация в строку
func (event *Event) ToString() string {
	b := strings.Builder{}
	b.WriteString(NewTag(BEGIN, VEVENT))
	for key, value := range event.components {
		b.WriteString(NewTag(key, value))
	}
	b.WriteString(NewTag(END, VEVENT))
	return b.String()
}

func NewTag(name string, value string) string {
	return fmt.Sprintf("%s:%s\n", name, value)
}

func EscapeString(text string) string {

	text = strings.ReplaceAll(text, "\\", "\\\\")
	text = strings.ReplaceAll(text, ";", `\;`)
	text = strings.ReplaceAll(text, ",", `\,`)
	text = strings.ReplaceAll(text, "\n", " ")
	return text
}
