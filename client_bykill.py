import random


class ClientByKill:
    def do_kill(self, value, weapon_dict, sockfd, addr, card_list):
        print(value, weapon_dict, addr, card_list)
        if abs(int(value)) == 17:
            weapon_dict["mount"] = None
            self.do_armor(2, sockfd, card_list, addr, weapon_dict, value)
        elif 18 <= abs(int(value)) <= 20:
            self.do_armor(2, sockfd, card_list, addr, weapon_dict, value)
        elif abs(int(value)) == 1 or abs(int(value)) == 16 or abs(int(value)) == 22:
            print("被杀")
            self.do_armor(2, sockfd, card_list, addr, weapon_dict, value)
        elif abs(int(value)) == 21:
            self.deal_card(2, sockfd, card_list, addr)

    def deal_card(self, num, sockfd, card_list, addr):
        print("判断是否出闪")
        for i in card_list:
            if abs(int(i)) == num:
                data = input("是否出牌")
                if data == "2":
                    sockfd.send("None", addr)
                    return
                else:
                    sockfd.send("True", addr)
                    card_list.remove(i)
                    return
        print("手牌中没有闪")
        sockfd.send("None", addr)

    def do_armor(self, num, sockfd, card_list, addr, weapon_dict, value):
        if weapon_dict["armor"] == "23":
            value = random.randint(1, 10)
            if value < 6:
                sockfd.send("True", addr)
                print("八卦生效")
            else:
                print("八卦失效")
                self.deal_card(num, sockfd, card_list, addr)
        elif weapon_dict["armor"] == "24":
            if int(value) < 0:
                sockfd.send("True", addr)
                print("仁王盾生效")
            else:
                self.deal_card(num, sockfd, card_list, addr)
        else:
            self.deal_card(num, sockfd, card_list, addr)
