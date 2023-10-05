package main

import (
	"context"
	"google.golang.org/grpc"
	"log"
	"net"
	pb "project/data/dis"
)

type Server struct {
	pb.UnimplementedAlgoServer
}

func (s *Server) GetDis(ctx context.Context, request *pb.DisRequest) (*pb.DisReply, error) {
	return &pb.DisReply{Dis: 123}, nil
}

func main() {
	lis, err := net.Listen("tcp", "127.0.0.1:50010")
	if err != nil {
		log.Fatalf("failed to listen: #{err}")
	}

	s := grpc.NewServer()

	pb.RegisterAlgoServer(s, &Server{})
	log.Printf("server listening at %v", lis.Addr())
	//pb2.RegisterGreeterServer(s, &pb2.Server{})

	if err := s.Serve(lis); err != nil {
		log.Fatalf("failed to serve: %v", err)
	}
}
