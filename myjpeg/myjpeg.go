package myjpeg

import (
	"bytes"
	"image"
	"image/jpeg"
	"log"
	"os"
)

func Encode(path string) []byte {
	file, err := os.Open(path)
	if err != nil {
		log.Fatalln("open file fail")
	}
	defer file.Close()
	img, _, err := image.Decode(file)
	if err != nil {
		log.Fatalln("img decode fail")
	}
	buf := bytes.Buffer{}
	jpeg.Encode(&buf, img, &jpeg.Options{Quality: 10})
	return buf.Bytes()
}

func Decode(path string, data []byte) {
	os.WriteFile(path, data, 0777)
}
