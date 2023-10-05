import cv2
import numpy as np
from IMService import IMService
from proto import gopython_pb2
from proto import gopython_pb2_grpc
import grpc
from concurrent import futures


class Server(gopython_pb2_grpc.AlgoServicer):
    def GetDis(self, request, context):
        print("get request, path = ", request.path)
        # 读取图片
        img = cv2.imread(request.path)
        # 灰度化
        grayImg = IMService.IMGray(img)
        # 二值化
        binImg = IMService.IMBin(grayImg)
        # 投影
        data = IMService.IMProject(binImg)
        # 距离计算
        dis = IMService.IMDisCal(data)
        return gopython_pb2.DisReply(dis=dis)



if __name__ == "__main__":
    port = "50010"
    print("hello")
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    gopython_pb2_grpc.add_AlgoServicer_to_server(Server(), server)
    server.add_insecure_port("[::]:" + port)
    print("server start")
    server.start()
    server.wait_for_termination()







    

    


    

