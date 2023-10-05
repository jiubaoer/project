package test

import (
	"fmt"
	"testing"
)

func TestDefault(t *testing.T) {
	a := byte(1)
	fmt.Println(a)
	fmt.Println(a == 1)
}
