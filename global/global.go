package global

import (
	"github.com/spf13/viper"
	"go.uber.org/zap"
	"gocv.io/x/gocv"
	"google.golang.org/grpc"
	"project/config"
	"project/lora"
	"project/utils"
	"fmt"
)

var (
	Cap	 *gocv.VideoCapture
	Port     *lora.Port
	Conf     *config.Config
	Logger   *zap.Logger
	Conn     *grpc.ClientConn
	NextPort int
	Flag 	 int
)

var (
	Img       = make(chan int)
	ImgGather = make(chan int)
	Heart     = make(chan int)
	Dis       = make(chan int)
	REC       = make(chan struct{})
)

func init() {
	InitCam()
	utils.InitConfig()
	NextPort = viper.GetInt("nextPort")
	Port = utils.InitPort()
	Logger = zap.NewExample()
	Conn = utils.InitConn()
}

func InitCam() {
	cap, err := gocv.OpenVideoCapture(0)
	if err != nil {
		fmt.Println("open cam fail")
	}else {
		fmt.Println("open cam success")
	}
	Cap = cap
}
	
