package test

import (
	"gocv.io/x/gocv"
	"log"
	"testing"
)

func TestGocv(t *testing.T) {
	cap, err := gocv.OpenVideoCapture(0)
	defer cap.Close()
	if err != nil {
		log.Fatalf("%v", err)
	}
	img := gocv.NewMat()
	win := gocv.NewWindow("hello")
	for {
		cap.Read(&img)
		win.IMShow(img)
		win.WaitKey(1)
	}
}
