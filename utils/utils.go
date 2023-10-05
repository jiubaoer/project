package utils

// ByteToAddr 字节转地址
func ByteToAddr(b []byte) int {
	return int(b[0])<<8 + int(b[1])
}

// AddrToByte 地址转字节
func AddrToByte(a int) []byte {
	return []byte{byte(a >> 8), byte(a & 255)}
}

func Min(a, b int) int {
	if a < b {
		return a
	}
	return b
}
