package handler

import (
	"github.com/gin-gonic/gin"
	"log"
	"mytickets/src/apperrors"
	"net/http"
	"strconv"
)

func (h *Handler) ParserList(c *gin.Context) {
	parsers, err := h.ParserService.List(c)
	if err != nil {
		log.Fatal(err.Error())
		err := apperrors.NewBadRequest("bad request")
		c.JSON(
			err.Status(), gin.H{
				"error": err,
			})
		return
	}

	c.JSON(http.StatusOK, parsers)

}

func (h *Handler) GetParser(c *gin.Context) {
	parserId, err := strconv.ParseInt(c.Param("parserId"), 10, 64)
	if err != nil {
		apiErr := apperrors.NewBadRequest("Bad id")
		c.JSON(
			apiErr.Status(), gin.H{
				"error": apiErr,
			})
		return
	}
	parser, err := h.ParserService.Get(c, parserId)
	if err != nil {
		apiErr := apperrors.NewNotFound("Not found", strconv.FormatInt(parserId, 10))
		c.JSON(
			apiErr.Status(), gin.H{
				"error": apiErr,
			})
		return
	}

	c.JSON(http.StatusOK, parser)
}
