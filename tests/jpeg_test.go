package test

import (
	"bytes"
	"fmt"
	"image"
	"image/jpeg"
	"log"
	"os"
	"testing"
)

func TestJpeg(t *testing.T) {
	file, err := os.Open("./src.jpeg")
	defer file.Close()
	if err != nil {
		log.Fatalf("%v", err)
	}
	img, _, err := image.Decode(file)
	if err != nil {
		log.Fatalf("%v", err)
	}
	buf := bytes.Buffer{}
	err = jpeg.Encode(&buf, img, &jpeg.Options{Quality: 10})
	if err != nil {
		log.Fatalf("%v", err)
	}
	os.WriteFile("./test.jpeg", buf.Bytes(), 0777)
	fmt.Println(len(buf.Bytes()))
}
