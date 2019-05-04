class ClientKill:
    def do_kill(self, data, sockfd, weapon_dict, addr, card_list):
        if weapon_dict["armor"] == "26" or weapon_dict["armor"] == "25":
            distance = "2"
        else:
            distance = "1"
        if weapon_dict["weapon"]:
            value = weapon_dict["weapon"]
            value = self.black(data, value)
            if abs(int(value)) == 18:
                self.zhangba(card_list, sockfd, addr, data)
                self.choose_player(sockfd)
            elif abs(int(value)) == 19:
                sockfd.send("S %s" % value, addr)
                self.choose_player(sockfd)
                card_list.remove(data)
                self.guanshi(sockfd, card_list)
            elif abs(int(value)) == 20:
                if self.fangtian(sockfd, card_list, value, addr):
                    self.choose_more(sockfd)
                else:
                    self.choose_player(sockfd)
                card_list.remove(data)
            elif abs(int(value)) == 22:
                sockfd.send("S %s" % value, addr)
                self.choose_player(sockfd)
                card_list.remove(data)
                self.qinglong(sockfd, card_list)
            elif abs(int(value)) == 16:
                sockfd.send("S %s %s" % (value, distance), addr)
                self.choose_player(sockfd)
                card_list.remove(data)
            else:
                sockfd.send("S %s" % value, addr)
                self.choose_player(sockfd)
                card_list.remove(data)
        else:
            sockfd.send("S %s %s" % (data, distance), addr)
            self.choose_player(sockfd)
            card_list.remove(data)

    def choose_player(self, sockfd):
        data, addr = sockfd.recv()
        while True:
            value = input("请选择击杀目标%s" % data)
            if value in data:
                sockfd.send(value, addr)
                return
            else:
                print("输入有误")

    def choose_more(self, sockfd):
        data, addr = sockfd.recv()
        print(data)
        while True:
            print("选择三位玩家")
            msg01 = input("选择第一位玩家：")
            msg02 = input("选择第二位玩家：")
            msg03 = input("选择第三位玩家：")
            if msg01 in data and msg02 in data and msg03 in data:
                sockfd.send("%s %s %s" % (msg01, msg02, msg03), addr)
                return
            else:
                print("输入有误")

    def black(self, data, value):
        if int(data) > 0:
            return value
        else:
            return str(-int(value))

    def red(self, data01, data02, value):
        if int(data01) < 0 and int(data02) < 0:
            return str(-int(value))
        else:
            return str(int(value))

    def zhangba(self, card_list, sockfd, addr, value):
        while True:
            data = input("是否使用丈八蛇矛")
            if data == "1" and len(card_list) >= 2:
                msg01 = input("请弃第一张牌")
                msg02 = input("请弃第二张牌")
                if msg01 in card_list and msg02 in card_list:
                    card_list.remove(msg01)
                    card_list.remove(msg02)
                    data = self.red(msg01, msg02, value)
                    sockfd.send("S %s %d" % (data, 3), addr)
                    break
                else:
                    print("有误")
            else:
                sockfd.send("S %s %d" % (value, 3), addr)
                card_list.remove(value)
                break

    def guanshi(self, sockfd, card_list):
        data, addr = sockfd.recv()
        if data == "True":
            while True:
                data = input("是否弃两张牌对其造成伤害")
                if data == "1" and len(card_list) >= 2:
                    msg01 = input("请弃第一张牌")
                    msg02 = input("请弃第二张牌")
                    if msg01 in card_list and msg02 in card_list:
                        card_list.remove(msg01)
                        card_list.remove(msg02)
                        sockfd.send("True", addr)
                        break
                    else:
                        print("有误")
                else:
                    sockfd.send("None", addr)
        else:
            sockfd.send("None", addr)

    def fangtian(self, sockfd, card_list, value, addr):
        if len(card_list) == 1:
            msg = input("是否使用方天化戟")
            if msg == "1":
                sockfd.send("S %s" % value, addr)
                return True
            else:
                sockfd.send("S 29", addr)
        else:
            sockfd.send("S 29", addr)

    def qinglong(self, sockfd, card_list):
        while True:
            data, addr = sockfd.recv()
            if data == "True":
                while True:
                    data = input("是否继续出杀")
                    if data == "1":
                        msg = input("请出杀")
                        if abs(int(msg)) == 1 and msg in card_list:
                            sockfd.send("S %s" % msg, addr)
                        else:
                            print("输入有误")
                    else:
                        sockfd.send("None", addr)
                        return
            else:
                sockfd.send("None", addr)
                return
