sudo mknod /dev/rfcomm0 c 216 0
echo "create rfcomm0 success"

sudo chmod 777 /dev/rfcomm0

sudo rfcomm watch /dev/rfcomm0 1 &
echo "start watch rfcomm"

cd /home/project/project/algorithm
sudo python3 main.py &
echo "start algorithm server"

sudo chmod 777 /dev/ttyUSB0
echo "change access success"

sudo /home/xgw/4G/Quectel_QConnectManager_Linux_V1.6.0.16/quectel-CM/quectel-CM &




