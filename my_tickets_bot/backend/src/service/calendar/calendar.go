package calendar

import (
	"os"
	"strings"
)

type Calendar struct {
	events []Event
}

// AddEvent Добавление события в каледарь
func (calendar *Calendar) AddEvent(event Event) {
	calendar.events = append(calendar.events, event)
}

func NewCalendar() Calendar {
	return Calendar{
		events: []Event{},
	}
}

// ToString сериаризация в строку
func (calendar *Calendar) ToString() string {
	var b strings.Builder
	b.WriteString(NewTag(BEGIN, VCALENDAR))
	b.WriteString(NewTag(VERSION, "2.0"))
	for _, event := range calendar.events {
		b.WriteString(event.ToString())
	}
	b.WriteString(NewTag(END, VCALENDAR))
	return b.String()
}

// Save сохранение календаря в файл
func (calendar *Calendar) Save(filename string) error {
	data := calendar.ToString()
	err := os.WriteFile(filename, []byte(data), 0666)
	return err
}
