package services

import (
	"bytes"
	"fmt"
	"io"
	"mime/multipart"
	"net/http"
	"os"
)

func SendImg(path string, name string) {
	file, err := os.Open(path)
	if err != nil {
		fmt.Println("open img fail")
	}
	defer file.Close()

	// 创建一个buffer存储表单数据
	var buffer bytes.Buffer
	writer := multipart.NewWriter(&buffer)

	// 创建表单字段并写入buffer中
	fileWriter, err := writer.CreateFormFile("image", name)
	if err != nil {
		fmt.Println("create fileWriter fail")
	}
	_, err = io.Copy(fileWriter, file)
	if err != nil {
		fmt.Println("write img fail")
	}
	err = writer.Close()
	if err != nil {
		fmt.Println("tail wrong")
	}
	url := "http://8.130.50.95:8080/upload_img"
	contentType := writer.FormDataContentType()
	_, err = http.Post(url, contentType, &buffer)
	//http.NewRequest("POST", url, &buffer)
	if err != nil {
		fmt.Println("write img fail")
	}
}

