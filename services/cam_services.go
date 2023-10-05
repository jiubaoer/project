package services

import (
        "github.com/spf13/viper"
        "gocv.io/x/gocv"
        "project/global"
        "sync"
	"fmt"
)

func Monitor(wg *sync.WaitGroup) {
        defer wg.Done()
        
        img := gocv.NewMat()
        for {
                sourcePort := <-global.ImgGather
		for i := 0; i < 10; i++ {
			global.Cap.Grab(1)
		}
                global.Cap.Read(&img)
                addr := viper.GetString("port.Addr")
                name := ""
                if global.Flag == 1 {
                        name = "./img/" + addr + "_left.jpeg"
                } else if global.Flag == 2 {
                        name = "./img/" + addr + "_right.jpeg"
                }else {
                        name = "./img/" + addr + "_monitor.jpeg"
                }
		fmt.Println(name)
                if !gocv.IMWrite(name, img) {
                        continue
                }
		if global.Flag == 0 {
			global.Img <- sourcePort
		}
        }
}

