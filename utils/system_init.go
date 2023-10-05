package utils

import (
	"fmt"
	"github.com/spf13/viper"
	"google.golang.org/grpc"
	"google.golang.org/grpc/credentials/insecure"
	"log"
	"project/lora"
)

func InitConfig() {
	viper.SetConfigName("config")
	viper.AddConfigPath("config")
	viper.AddConfigPath("../config")
	err := viper.ReadInConfig()
	if err != nil {
		fmt.Println("读取配文件失败")
	}
}

func InitPort() *lora.Port {
	cfg := lora.Config{
		Name:        viper.GetString("port.Name"),
		Baud:        viper.GetInt("port.Baud"),
		Addr:        viper.GetInt("port.Addr"),
		ReadTimeout: viper.GetDuration("port.ReadTimeout"),
	}

	port, err := lora.OpenPort(cfg)
	if err != nil {
		fmt.Println("打开串口失败")
	}
	return port
}

func InitConn() *grpc.ClientConn {
	conn, err := grpc.Dial("127.0.0.1:50010", grpc.WithTransportCredentials(insecure.NewCredentials()))
	if err != nil {
		log.Fatalf("did not connect: %v", err)
	}
	defer conn.Close()

	return conn
}
