package services

import (
	"context"
	"github.com/spf13/viper"
	"go.uber.org/zap"
	"google.golang.org/grpc"
	"google.golang.org/grpc/credentials/insecure"
	"log"
	"project/data/dis"
	"project/global"
	"time"
)

func GetDis() int32 {
	conn, err := grpc.Dial("127.0.0.1:50010", grpc.WithTransportCredentials(insecure.NewCredentials()))
	if err != nil {
		log.Fatalf("did not connect: %v", err)
	}
	defer conn.Close()

	ctx, cancel := context.WithTimeout(context.Background(), time.Second)
	defer cancel()

	c := dis.NewAlgoClient(conn)
	global.Logger.Info("get dis data",
		zap.Time("time", time.Now()),
	)
	r, _ := c.GetDis(ctx, &dis.DisRequest{Path: "." + viper.GetString("img.monitor")})
	return r.GetDis()
}
