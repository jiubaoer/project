package config

import "time"

type Config struct {
	Port PortConfig
}

type PortConfig struct {
	Name        string
	Baud        int
	ReadTimeout time.Duration
	Addr        int
}
