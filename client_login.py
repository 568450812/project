
from hero_01 import *

class ClientL:
    def __init__(self):
        self.sockfd = Connect()
        self.addr = (("0.0.0.0",10010))
        self.hero = None
    # 登录操作
    def do_login(self, name, passwd):
        value = "L %s %s" % (name, passwd)
        self.sockfd.send(value, self.addr)
        data, addr = self.sockfd.recv()
        if data == "OK":
            print("匹配中")
            self.choose_hero()
        else:
            print(data)

    # 根据服务端发送英雄选择英雄
    def choose_hero(self):
        data, addr = self.sockfd.recv()  # 客户端发送三个英雄
        herolist = data.split(" ")
        print(herolist[0], herolist[1], herolist[2],herolist[3])
        while True:
            value = input("请选择武将:")
            if value in herolist:
                print(self.addr)
                self.sockfd.send(value, self.addr)  # 选择其中一个发送给服务端
                return
            else:
                print("输入有误")

    # 接收英雄类
    def recv_hero(self):
        data, addr = self.sockfd.recv()  # 服务端返回一个英雄
        print(data)
        self.hero = eval(data)  # 绑定英雄类

if __name__ == "__main__":
    s = ClientL()
    s.do_login("123456", "123456")
    s.recv_hero()
    s.hero.do_request()
