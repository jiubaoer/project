package lora

import (
	"errors"
	"fmt"
	"github.com/tarm/serial"
	"time"
)

// 包头数据长度 / 字节
var (
	sourcePortSize      = 2
	destinationPortSize = 2
	orderNumberSize     = 4
	ackNumberSize       = 4
	flagSize            = 1
	packSize            = 2
	checkSumSize        = 2
	headSize            = 17
)

var (
	sourcePortBegin      = 0
	destinationPortBegin = 2
	orderNumberBegin     = 4
	ackNumberBegin       = 8
	flagBegin            = 12
	packSizeBegin        = 13
	checkSumBegin        = 15
)

var (
	// 包数据最大长度
	maxPack = 240
)

type Config struct {
	Name        string
	Baud        int
	Addr        int
	ReadTimeout time.Duration
}

type Port struct {
	Addr int
	port *serial.Port
}

func OpenPort(config Config) (*Port, error) {
	c := &serial.Config{
		Name:        config.Name,
		Baud:        config.Baud,
		ReadTimeout: config.ReadTimeout,
	}
	port, err := serial.OpenPort(c)
	if err != nil {
		return nil, err
	}
	return &Port{
		port: port,
		Addr: config.Addr,
	}, nil
}

func genPackage(sourcePort, destinationPort, orderNumber, ackNumber, flag int, dataBody []byte) []byte {
	l := headSize + len(dataBody)
	pack := make([]byte, 0, l)
	// 源端口
	for i := sourcePortSize - 1; i >= 0; i-- {
		pack = append(pack, byte(sourcePort>>(i*8)))
	}
	// 目标端口
	for i := destinationPortSize - 1; i >= 0; i-- {
		pack = append(pack, byte(destinationPort>>(i*8)))
	}
	// 序号
	for i := orderNumberSize - 1; i >= 0; i-- {
		pack = append(pack, byte(orderNumber>>(i*8)))
	}
	// 确认号
	for i := ackNumberSize - 1; i >= 0; i-- {
		pack = append(pack, byte(ackNumber>>(i*8)))
	}
	// flag
	for i := flagSize - 1; i >= 0; i-- {
		pack = append(pack, byte(flag>>(i*8)))
	}
	// 包长
	for i := packSize - 1; i >= 0; i-- {
		pack = append(pack, byte(l>>(i*8)))
	}
	// 检验和
	var sum int
	for _, b := range pack {
		sum += int(b)
	}

	for _, b := range dataBody {
		sum += int(b)
	}

	for i := checkSumSize - 1; i >= 0; i-- {
		pack = append(pack, byte(sum>>(i*8)))
	}

	pack = append(pack, dataBody...)

	return pack
}

// 检验包准确性
func checkSum(sum int, data []byte) bool {
	var temp int
	for i, b := range data {
		if i == headSize-1 || i == headSize-2 {
			continue
		}
		temp += int(b)
	}
	return temp == sum
}

// 包长和数据 保证同一时刻只会收到一个包
func (p *Port) receivePackage() (int, []byte) {
	data := make([]byte, 0, 500)
	buf := make([]byte, 500)
	l, sum, timer := 0, -1, 0
	for {
		n, _ := p.port.Read(buf)
		if n == 0 {
			time.Sleep(time.Second)
			timer++
		} else {
			l += n
			data = append(data, buf[:n]...)
			timer = 0
		}

		if len(data) >= headSize {
			sum = int(data[packSizeBegin])<<8 + int(data[packSizeBegin+1])
		}

		if timer == 5 || l == sum {
			break
		}
	}

	return l, data[:l]
}

// SendData 发送数据
// flag
// 1 << 0 结束包
// 1 << 1 tcp
// 1 << 2 ack
func (p *Port) SendData(des int, data []byte, network string) {
	n, start, order, resend := len(data), 0, 1, 0

	for {
		if start >= n {
			return
		}
		end, flag := start+maxPack, 0
		if network == "tcp" {
			flag += 1 << 1
		}
		if start+maxPack >= n {
			end = n
			flag += 1
		}
		pack := genPackage(p.Addr, des, order, 0, flag, data[start:end])
		p.port.Write(pack)
		fmt.Println("send data, 序号: ", order, "长度：", len(pack))
		if network == "tcp" {
			_, ack, _ := p.ReceiveData()
			ackNum := int(ack[0])<<24 + int(ack[1])<<16 + int(ack[2])<<8 + int(ack[3])
			if ackNum == order {
				start += maxPack
				order++
				fmt.Println("receive ack, 序号: ", ackNum)
			} else {
				resend++
				fmt.Println("reSend", resend)
			}
		} else {
			start += maxPack
		}

		time.Sleep(time.Millisecond * 500)
	}

}

// ReceiveData 接收数据来源端口, 数据
func (p *Port) ReceiveData() (int, []byte, error) {
	dataLen, data, sourcePort := 0, make([]byte, 0, 500), 0

	for {
		// 接收包
		n, pack := p.receivePackage()
		// 合理性校验
		if n < headSize {
			fmt.Println(errors.New("receive data, 未达到包头长度"))
			continue
		}
		l := int(pack[headSize-4])<<8 + int(pack[headSize-3])
		if l != n {
			fmt.Println(errors.New("receive data, 数据包长度错误"))
			continue
		}
		sum := int(pack[headSize-2])<<8 + int(pack[headSize-1])
		if !checkSum(sum, pack) {
			fmt.Println(errors.New("receive data, 未通过检验和"))
		}
		receivePort := int(pack[2])<<8 + int(pack[3])
		if receivePort != p.Addr {
			fmt.Println(errors.New("receive data, 接收包地址错误"))
			continue
		}

		// 根据包的情况进行分类
		flag := pack[flagBegin]
		sourcePort = int(pack[0])<<8 + int(pack[1])

		// ack包
		if (flag>>2)&1 == 1 {
			return sourcePort, pack[ackNumberBegin : ackNumberBegin+ackNumberSize], nil
		}

		dataLen += n - headSize
		data = append(data, pack[headSize:]...)
		// 回复ack包
		if (flag>>1)&1 == 1 {
			orderNumber := 0
			for i := 0; i < orderNumberSize; i++ {
				orderNumber += int(pack[orderNumberBegin+i]) << ((orderNumberSize - i - 1) * 8)
			}
			fmt.Println("receive data, 序号: ", orderNumber)
			ackPack := genPackage(p.Addr, sourcePort, 0, orderNumber, 1<<2, []byte{})
			p.port.Write(ackPack)
			fmt.Println("send ackPack， 长度：", len(ackPack))

		}
		// 如果是结束包, over
		if flag&1 == 1 {
			break
		}
	}
	// 数据包
	return sourcePort, data[:dataLen], nil
}
