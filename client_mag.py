from connect03 import *
from client_bykill import *
from client_kill import *


class ClientM:
    def __init__(self):
        self.sockfd = Connect()  # 建立连接
        self.addr = ("0.0.0.0", 10010)
        self.by_kill = ClientByKill()  # 收到杀的处理
        self.kill = ClientKill()  # 出杀的处理
        self.card_list = []  # 手牌列表
        self.status_list = []  # 判定列表
        self.weapon_dict = {"weapon": None, "mount": None, "armor": None}  # 装备字典
        self.used_list = []  # 用过的牌的列表

    # 处理客户端请求
    def do_request(self):
        self.sockfd.send("OK",self.addr)
        while True:
            data, addr = self.sockfd.recv()
            value = data.split(" ")
            print(value)
            if value[0] == "P":  # 初始发牌时的协议　将４张牌存入手牌
                self.card_list = [value[1], value[2], value[3], value[4]]  # 客户端发牌
                print(self.card_list)
            elif value[0] == "Q":  # 回合开始时出牌指令
                self.card_list += [value[1], value[2]]  # 客户端发牌　
                print(self.card_list)
                self.do_card()  # 进入出牌阶段
            elif value[0] == "C":  # 回合中的继续出牌指令
                print(self.card_list)
                self.do_card()
            elif value[0] == "S":  # 当被当成目标使用杀时　将细节交给by_kill模块执行
                self.by_kill.do_kill(value[1], self.weapon_dict, self.sockfd, self.addr, self.card_list)
            elif value[0] == "NM":  # 当被当成目标使用南蛮入侵时 参数表示必须要出的牌 1为杀
                self.deal_card(1)
            elif value[0] == "W":  # 当其他玩家使用锦囊牌时　判断是否使用无懈可击
                self.deal_card(8)
            elif value[0] == "SS":  # 当被当成目标使用顺手牵羊时
                self.do_shunshou()
            elif value[0] == "GH":  # 当被当成目标使用过河拆桥时
                self.do_guohe()
            elif value[0] == "JD":  # 当被当成目标使用决斗时
                self.do_juedou()
            elif value[0] == "WG":  # 当被当成目标使用五谷丰登时
                value.remove("WG")
                self.do_wugu(value)
            elif value[0] == "WJ":  # 当被当成目标使用万箭齐发时
                self.deal_card(2)
            elif value[0] == "A":  # 当计算距离时判断是否有马
                self.do_armor()
            elif value[0] == "J":
                self.do_help(value[1])
            elif value[0] == "G":
                print("你死啦")
                return

    def do_help(self,value):
        data = input("是否使用桃救%s"%value)
        if abs(int(data)) == 3 and data in self.card_list:
            self.sockfd.send("True",self.addr)
            self.card_list.remove(data)
        else:
            self.sockfd.send("None",self.addr)

    # 是否打出无懈可击
    def deal_card(self, msg):
        if msg == 1:
            value = "杀"
        else:
            value = "无懈可击"
        for i in self.card_list:
            if abs(int(i)) == msg:  # 判断手牌是否有无懈可击
                data = input("是否使用%s"%value)
                if data == "2":  # 选择不出发送none
                    self.sockfd.send("None", self.addr)
                    return
                else:
                    self.sockfd.send("True", self.addr)  # 出则发送true
                    self.card_list.remove(i)  # 出完需要移除此牌
                    return
        self.sockfd.send("None", self.addr)  # 如果手牌中没有无懈可击　则直接发送Ｎｏｎｅ

    # 服务端发送顺手牵羊指令
    def do_shunshou(self):
        list01 = [str(i) for i in range(len(self.card_list))]  # 将手牌索引传入列表
        list02 = [str(self.weapon_dict[i]) for i in self.weapon_dict if self.weapon_dict[i]]  # 将装备直接存入第二个列表
        self.sockfd.send("%s\n%s" % (" ".join(list01), " ".join(list02)), self.addr)  # 将两个列表一起发给服务端　供选择
        data, addr = self.sockfd.recv()  # 出牌方选择的牌
        value = data.split(" ")
        if data[0] == "1":
            self.sockfd.send(self.card_list.pop(int(value[1])), self.addr)  # 第一行表示手排列表　发送回去并移除
        elif data[0] == "2":  # 第二行为装备列表　将装备直接发送后移除
            value = self.do_dict(value[1])
            self.sockfd.send(self.weapon_dict[value], self.addr)
            self.weapon_dict[value] = None

    # 服务端发送过河拆桥指令
    def do_guohe(self):
        list01 = [str(i) for i in range(len(self.card_list))]  # 将手牌索引传入列表
        list02 = [str(self.weapon_dict[i]) for i in self.weapon_dict if self.weapon_dict[i]]  # 将装备直接存入第二个列表
        self.sockfd.send("%s\n%s" % (" ".join(list01), " ".join(list02)), self.addr)  # 将两个列表一起发给服务端　供选择
        data, addr = self.sockfd.recv()
        value = data.split(" ")
        if data[0] == "1":  # 第一行表示手排列表 直接移除
            self.card_list.pop(int(value[1]))
        elif data[0] == "2":  # 第二行为装备列表　将装备直接移除
            value = self.do_dict(value[1])
            self.weapon_dict[value] = None

    def do_armor(self):
        if self.weapon_dict["armor"] == "27" or self.weapon_dict["armor"] == "28":  # 判断装备列表中是否又＋１马
            self.sockfd.send("True", self.addr)  # 有则发送Ｔｒｕｅ
        else:
            self.sockfd.send("None", self.addr)

    # 执行五谷丰登
    def do_wugu(self,list01):
        print(list01)
        while True:
            value = input("请输入想要选择的牌")
            if value in list01:
                self.sockfd.send(value, self.addr)
                self.card_list.append(value)
                return
            else:
                print("输入有误")

    # 执行决斗
    def do_juedou(self):
        print(self.card_list)
        while True:
            value = input("出杀请输1或-1,没有请输2")
            if value in self.card_list and abs(int(value)) == 1:
                self.sockfd.send(value, self.addr)
                self.card_list.remove(value)
                return
            elif abs(int(value)) == 2:
                self.sockfd.send(value, self.addr)
                return
            else:
                print("输入有误")

    # 出牌阶段
    def do_card(self):
        while True:
            data = input("选择要出的牌")
            if data == "#":
                self.choose_card(data)
                return
            elif abs(int(data)) == 1:
                if self.used_card(data):
                    print("一个回合只能出一次杀")
                    continue
                else:
                    self.choose_card(data)
                    return
            # elif data not in self.card_list:
            #     print("输入有误")
            #     continue
            else:
                self.choose_card(data)
                return

    # 根据出的牌进行处理
    def choose_card(self, data):
        if data == "#":  # 如果输入井号　则结束回合　清空使用牌的列表　执行弃牌操作
            self.used_list.clear()
            self.abonden_card()
            return
        elif abs(int(data)) == 1:  # 如果出杀则调用杀类处理
            self.kill.do_kill(data, self.sockfd, self.weapon_dict, self.addr, self.card_list)
        elif 4 <= abs(int(data)) < 8 or abs(int(data)) == 12:  # 使用锦囊
            self.sockfd.send("EX %s" % data, self.addr)
            self.card_list.remove(data)
        elif abs(int(data)) == 3:  # 使用桃
            self.sockfd.send("T", self.addr)
            self.card_list.remove(data)
        elif abs(int(data)) == 9:  # 使用锦囊
            self.sockfd.send("EX %s" % data, self.addr)
            msg01 = self.recv_shunshou()
            self.recv_card(msg01)
            self.card_list.remove(data)
        elif abs(int(data)) == 10:  # 使用锦囊顺手牵羊
            self.sockfd.send("EX %s" % data, self.addr)
            self.recv_shunshou()
            self.card_list.remove(data)
        elif abs(int(data)) == 11:  # 使用锦囊过河拆桥
            self.sockfd.send("EX %s" % data, self.addr)
            self.recv_juedou()
            self.card_list.remove(data)
        elif 16 <= abs(int(data)) <= 28:  # 装备牌　直接存入装备字典
            self.weapon_dict[self.do_dict(data)] = data
            # self.card_list.remove(data)
            print(self.weapon_dict)
            self.do_card()
        else:
            print("不合法出牌")
            self.do_card()

    # 出顺手牵羊
    def recv_shunshou(self):
        data, addr = self.sockfd.recv()
        print(data)
        while True:
            value = input("请选择哪一位玩家")
            if value in data:
                self.sockfd.send(value, addr)
                data, addr = self.sockfd.recv()
                print(data)
                while True:
                    msg01 = input("请选择第几行")
                    msg02 = input("选择哪一个")
                    if 1 <= int(msg01) <= 2 and msg02 in data:
                        self.sockfd.send("%s %s" % (msg01, msg02), addr)
                        return msg01
                    else:
                        print("输入有误")
            else:
                print("输入有误")

    # 处理顺手牵羊接到的牌
    def recv_card(self, msg01):
        data, addr = self.sockfd.recv()
        if msg01 == "1":
            self.card_list.append(data)
        else:
            value = self.do_dict(data)
            self.weapon_dict[value] = data

    # 发送决斗
    def recv_juedou(self):
        data, addr = self.sockfd.recv()
        print(data)
        while True:
            value = input("请选择哪一位玩家")
            if value in data:
                self.sockfd.send(value, self.addr)
                return
            else:
                print("输入有误")

    # 本回合使用的手牌 如果已经出过杀 则不能再出
    def used_card(self, data):
        if self.weapon_dict["weapon"] != "16" and abs(int(data)) in self.used_list:
            return True
        else:
            self.used_list.append(abs(int(data)))
            return False


    # 回合结束时需弃到跟本身血量一样数量的牌
    def abonden_card(self):
        self.sockfd.send("#", self.addr)
        data, addr = self.sockfd.recv()
        print(data)
        if len(self.card_list) > int(data):
            while (len(self.card_list) - int(data)) > 0:
                value = input("请弃牌")
                if value in self.card_list:
                    self.card_list.remove(value)
                else:
                    print("有误")
            self.sockfd.send("#", addr)
        else:
            self.sockfd.send("#", addr)

    # 判断装备类型 武器　防具　坐骑
    def do_dict(self, value):
        if 16 <= int(value) <= 22:
            return "weapon"
        elif 23 <= int(value) <= 24:
            return "armor"
        elif 25 <= int(value) <= 28:
            return "mount"


