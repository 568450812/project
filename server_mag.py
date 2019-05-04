"""
服务器端用户处理
"""
from mysql_05 import *
from helper_d import *
from connect03 import *
import random
from seaver_kill import *
from server_ex import *

address = "0.0.0.0"
port = 10010
port01 = 10010
addr = (address, port01)


class ServerM:
    def __init__(self):
        self.mysql = MenberManage()  # 连接数据库
        self.sockfd = Connect()  # 调用连接
        self.sockfd.bind(addr)
        self.card_list = card_list  # 调用牌库
        self.hero_list = hero_list  # 调用英雄列表
        self.dict01 = {}  # 存储位置和地址
        self.player_list = ["p1", "p2", "p3", "p4", "p5"]  # 位置列表
        self.actor_dict = self.do_dict()
        self.kill = ServerKill()
        self.ex = ServerEX()

    def do_dict(self):
        list01 = self.player_list.copy()
        random.shuffle(list01)
        list01.remove("p1")
        dict01 = {"a": ["p1"], "b": [], "c": [], "d": []}
        dict01["b"].append(list01[-1])
        dict01["c"].append(list01[-2])
        dict01["c"].append(list01[-3])
        dict01["d"].append(list01[-4])
        return dict01

    def do_actor(self, id):
        for i in self.actor_dict:
            if id in self.actor_dict[i]:
                return i

    # 登录操作
    def do_login(self, id, passwd, addr):
        if self.mysql.select_passwd(id, passwd):  # 查询用户名密码是否匹配　匹配返回TRUE
            self.give_id(addr)
            self.sockfd.send("OK", addr)
        else:
            value = "登录失败帐号或密码错误"
            self.sockfd.send(value, addr)

    # 向各服务端分配位置
    def give_id(self, addr):
        while True:
            value = random.randint(1, 5)
            if "p%d" % value not in self.dict01:
                self.dict01["p%d" % value] = addr  # 将地址和位置存入字典
                break

    # 将初始４张牌发送
    def send_play(self):
        random.shuffle(self.card_list)
        for i in self.player_list:
            data = "P %s %s %s %s" % (
                self.card_list.pop(-1), self.card_list.pop(-2), self.card_list.pop(-3), self.card_list.pop(-4))
            self.sockfd.send(data, self.dict01[i])

    # 将3个英雄编号随机发送给玩家
    def send_hero(self):
        self.hero_list = self.hero_list[3:]
        random.shuffle(self.hero_list)
        for i in self.dict01:
            if i == "p1":
                self.sockfd.send("1 2 3 a", self.dict01[i])
            else:
                data = "%s %s %s %s" % (
                self.hero_list.pop(-1), self.hero_list.pop(-2), self.hero_list.pop(-3), self.do_actor(i))
                print(data)
                self.sockfd.send(data, self.dict01[i])

    # 等待所有用户选择英雄并通过数据库连接返回英雄
    def recv_hero(self):
        for i in range(5):
            data, addr = self.sockfd.recv()
            print(data)
            value = self.mysql.select_hero(data)
            print(value)
            self.sockfd.send(value, addr)

    def do_request(self):
        # self.do_apply()
        print(self.dict01)
        self.send_hero()  # 选择英雄
        self.recv_hero()  # 发送英雄
        self.send_play()
        self.do_putcard()

    def find_player(self, addr):
        for i in self.dict01:
            if self.dict01[i] == addr:
                return i

    def tao(self, addr):
        data = self.find_player(addr)
        if self.kill.dict02[data] < self.kill.dict01[data]:
            self.kill.dict02[data] += 1
            print(self.kill.dict02)

    def get_wuxie(self, list01, id, value):
        for i in list01:
            self.sockfd.send("W %s %s" % (id, value), self.dict01[i])
            data, addr = self.sockfd.recv()
            if data == "Ture":
                return
        return True

    # 处理用户请求
    def do_connect(self):
        while True:
            data, addr = self.sockfd.recv()
            print(data)
            value = data.split(" ")
            if value[0] == "L":  # 登录操作
                self.do_login(value[1], value[2], addr)  # 帐号密码
                if len(self.dict01) == 5:
                    return

    def do_list(self, id):
        list01 = self.player_list.copy()
        num = list01.index(id)
        list02 = list01[num + 1:] + list01[:num]
        return list02

    def do_putcard(self):
        while True:
            for i in self.player_list:
                self.put_card(i,card_list)
                while True:
                    value, addr = self.sockfd.recv()
                    id = self.find_player(addr)
                    list01 = self.do_list(id)
                    data = value.split(" ")
                    print(value)
                    if data[0] == "S":
                        self.kill.do_kill(id, self.sockfd, addr, data, self.dict01, list01,self.do_hp)
                        self.sockfd.send("C", addr)
                    elif data[0] == "EX":
                        if self.get_wuxie(list01, id, value):
                            self.ex.check_card(data[1], list01, self.card_list,self.sockfd, addr,\
                                               self.kill.dict02, self.kill.dict01, self.dict01,self.do_hp)
                            if abs(int(data[1])) != 4:
                                self.sockfd.send("C", addr)
                        else:
                            self.sockfd.send("C", addr)
                    elif data[0] == "T":
                        self.tao(addr)
                        self.sockfd.send("C", addr)
                    elif data[0] == "#":
                        self.sockfd.send(str(self.kill.dict02[i]), addr)
                        data, addr = self.sockfd.recv()
                        if data == "#":
                            break

    def game_result(self):
        if len(self.actor_dict["a"]) == 0 and len(self.actor_dict["b"]) != 0:
            print("反贼胜利")
        elif len(self.actor_dict["a"]) == 0 and len(self.actor_dict["b"]) == 0:
            print("奸臣胜利")
        elif len(self.actor_dict["b"]) == 0 and len(self.actor_dict["c"]) == 0:
            print("好人胜利")

    def do_hp(self, id):
        list01 = self.player_list.copy()
        num = list01.index(id)
        list02 = list01[num:] + list01[:num]
        for i in list02:
            self.sockfd.send("J %s" % id, self.dict01[i])
            data, addr = self.sockfd.recv()
            if data == "True":
                return
        self.sockfd.send("G %s" % id, self.dict01[id])
        del self.dict01[id]
        self.actor_dict[self.do_actor(id)].remove(id)
        self.game_result()

    def put_card(self,i,card_list):
        if len(self.card_list) <= 5:
            random.shuffle(card_list)
            self.card_list += card_list
        data = "Q %s %s" % (self.card_list[-1], self.card_list[-2])
        self.sockfd.send(data, self.dict01[i])





if __name__ == "__main__":
    s = ServerM()
    s.do_connect()
    s.do_request()
