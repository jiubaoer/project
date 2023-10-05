package test

import (
	"project/global"
	"testing"
)

func TestLora(t *testing.T) {
	data := []byte("hello")
	global.Port.Write(data)
}
