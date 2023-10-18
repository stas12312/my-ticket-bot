package handler

import (
	"github.com/stretchr/testify/assert"
	"mytickets/src/model"
	"testing"
)

func TestMakeDescription(t *testing.T) {
	expected := "📍 Moscow, Lenina 1\n🔗 https://link.com"
	event := model.Event{
		Location: model.Location{
			Id:      1,
			Name:    "Cinema",
			Address: "Lenina 1",
			Url:     "",
			City: model.City{
				Name: "Moscow",
			},
		},
		Link: "https://link.com",
	}
	actual := MakeDescription(&event)

	assert.Equal(t, expected, actual)
}
