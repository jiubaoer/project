package test

import (
	"context"
	"google.golang.org/grpc"
	"google.golang.org/grpc/credentials/insecure"
	"log"
	"project/data/dis"
	"testing"
	"time"
)

func TestDis(t *testing.T) {
	conn, err := grpc.Dial("127.0.0.1:50010", grpc.WithTransportCredentials(insecure.NewCredentials()))
	if err != nil {
		log.Fatalf("did not connect: %v", err)
	}
	defer conn.Close()
	ctx, cancel := context.WithTimeout(context.Background(), time.Second)
	defer cancel()
	c := dis.NewAlgoClient(conn)
	r, _ := c.GetDis(ctx, &dis.DisRequest{Path: "asfd"})
	log.Println(r.GetDis())
}
