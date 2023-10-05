package main

import (
	"project/global"
	"project/services"
	"sync"
	"fmt"
)

func main() {
	defer global.Cap.Close()
	fmt.Println("start...")
	wg := sync.WaitGroup{}
	wg.Add(4)

	// 获取蓝牙通知
	go services.GetBluetooth(&wg)

	// 摄像头采集图像
	go services.Monitor(&wg)

	// 发送消息
	go services.SendProc(&wg)

	// 接收消息
	go services.ReceiveProc(&wg)

	wg.Wait()
}
