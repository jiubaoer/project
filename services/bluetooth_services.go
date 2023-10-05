package services

import (
	"fmt"
	"project/global"
	serial "github.com/tarm/goserial"
	"sync"
	"time"
)

func GetBluetooth(wg *sync.WaitGroup) {
	defer wg.Done()
	config := &serial.Config{
		Name: "/dev/rfcomm0",
		Baud: 115200,
	}

	port, err := serial.OpenPort(config)
	if err != nil {
		fmt.Println("open bluetooth fail")
	}else {
		fmt.Println("open bluetooth success...")
		fmt.Println("watch bluetooth...")
	}

	for {
		
		buffer := make([]byte, 100)
		n, err := port.Read(buffer)
		if err != nil {
			time.Sleep(time.Second)
			continue
		}
		fmt.Println(n)
		fmt.Println("accept message", string(buffer[:n]))
		
		// 解析消息
		if buffer[0] == byte(0) {
			global.Flag = 0
			fmt.Println("config")
		}
		
		// 更改配置文件

		// 采集图像
		// 调用摄像头采集定位图像
		if n == 1 && buffer[0] == byte(1) {
			global.Flag = 1
			fmt.Println("left")
			global.ImgGather <- 0
		}

		// 调用摄像头采集反位图像
		if n == 1 && buffer[0] == byte(2) {
			global.Flag = 2
			fmt.Println("right")
			global.ImgGather <- 0
		}

		// 收集图像， 将图像发到监控端， 具体为 addr_left（定位）/right（反位）_img

	}

}
