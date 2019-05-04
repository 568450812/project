from socket import *


class Connect:
    def __init__(self):
        self.sockfd = socket(AF_INET, SOCK_DGRAM)  # 建立套接字

    def __del__(self):
        self.sockfd.close()  # 关闭套接字

    # 绑定地址
    def bind(self, addr):
        self.sockfd.bind(addr)

    # 重写接收消息方法
    def recv(self):
        data, addr = self.sockfd.recvfrom(1024)
        return (data.decode(), addr)

    # 重写发送消息方法
    def send(self, data, addr):
        self.sockfd.sendto(data.encode(), addr)