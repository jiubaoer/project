package services

import (
	"fmt"
	"go.uber.org/zap"
	"project/global"
	"project/myjpeg"
	"strconv"
	"sync"
	"time"
	"math/rand"
	"github.com/spf13/viper"
)

func sendMsg(desPort int, c string) {
	data := []byte(c)
	global.Port.SendData(desPort, data, "udp")
	global.Logger.Info("Lora模块发送信息",
		zap.Time("time", time.Now()),
		zap.Namespace("LoraMsg"),
		zap.Int("address", desPort),
		zap.String("msg", c),
		zap.ByteString("dataPkg", data),
	)
}

func sendImg(desPort int, path string) {
	data := myjpeg.Encode(path)
	global.Logger.Info("Lora模块发送图片",
		zap.Time("time", time.Now()),
		zap.Int("imgLen", len(data)),
	)
	global.Port.SendData(desPort, data, "tcp")
}

func SendProc(wg *sync.WaitGroup) {
	defer wg.Done()
	for {
		select {
		case desPort := <-global.Img:
			left := viper.GetString("port.Addr") + "_left.jpeg"
			right := viper.GetString("port.Addr") + "_right.jpeg"
			name := viper.GetString("port.Addr") + "_monitor.jpeg"
			path_left := "./img/" + left
			path_right := "./img/" + right
			path := "./img/" + name
			if desPort == 0 {
				SendImg(path_left, left)
				SendImg(path_right, right)
				SendImg(path, name)
			}else {
				sendImg(desPort, path)
			}
			global.REC <- struct{}{}
		case desPort := <-global.Dis:
			dis := int32(rand.Intn(10))
			dis = GetDis()
			//dis = int32(rand.Intn(10))
			sendMsg(desPort, strconv.Itoa(int(dis)))
			global.REC <- struct{}{}
		case desPort := <-global.Heart:
			sendMsg(desPort, "ok")
			global.REC <- struct{}{}
		}
	}
}

func ReceiveProc(wg *sync.WaitGroup) {
	defer wg.Done()
	for {
		sourcePort, data, err := global.Port.ReceiveData()
		fmt.Println(sourcePort, string(data))
		if err != nil {
			fmt.Println(err)
			continue
		}
		switch data[0] {
		//	距离包
		case 'd':
			global.Dis <- sourcePort
			<-global.REC
		// 图片包
		case 'i':
			if data[3] == '1' {
				sourcePort = 0
			}
			global.Flag = 0
			global.ImgGather <- sourcePort
			<-global.REC
			// 图片包
		case 'h':
			global.Heart <- sourcePort
			<-global.REC
		}
	}
}
