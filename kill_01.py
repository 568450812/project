from client_mag import *

class Kill:
    def __init__(self):
        self.sockfd = ClientM()
        self.addr = ("0.0.0.0",10010)

    def kill(self,sockfd):
        sockfd.send("K",self.addr)
        data,addr = sockfd.recv()
        list01 = data.split(" ")
        print(list01)
        while True:
            value = input("选择目标")
            if value in list01:
                sockfd.send(value,self.addr)
                break
            else:
                print("输入有误")
        data,addr = sockfd.recv()
        print(data)



