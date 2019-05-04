class ServerEX:
    def check_card(self, card, list01, card_list, sockfd, addr, dict02, dict01, dict03, do_hp):
        if abs(int(card)) == 4:
            self.wuzhong(card_list, sockfd, addr)
        elif abs(int(card)) == 5:
            self.taoyuan(dict02, dict01)
        elif abs(int(card)) == 6:
            self.nanman(list01, sockfd, dict03, dict02)
        elif abs(int(card)) == 7:
            self.wanjian(list01, sockfd, dict03, dict02)
        elif abs(int(card)) == 9:
            self.shunshou(list01, sockfd, addr, dict03)
        elif abs(int(card)) == 10:
            self.guohe(list01, sockfd, addr, dict03)
        elif abs(int(card)) == 11:
            self.juedou(list01, sockfd, addr, dict03, dict02)
        elif abs(int(card)) == 12:
            self.wugu(card_list, sockfd, list01, dict03)
        elif abs(int(card)) == 13:
            pass
        elif abs(int(card)) == 14:
            pass
        i = self.find_nohp(dict02)
        if i:
            do_hp(i)
        else:
            return

    def find_play(self, dict03, list01):
        for i in dict03:
            if i not in list01:
                return i

    def wuzhong(self, list01, sockfd, addr):
        sockfd.send("Q %s %s" % (list01.pop(-1), list01.pop(-2)), addr)

    def taoyuan(self, dict02, dict01):
        for i in dict02:
            if dict02[i] < dict01[i]:
                dict02[i] += 1
        print(dict02)

    def nanman(self, list01, sockfd, dict03, dict02):
        for i in list01:
            sockfd.send("NM", dict03[i])
            data, addr = sockfd.recv()
            if data == "None":
                dict02[i] -= 1
                print(dict02)

    def wanjian(self, list01, sockfd, dict03, dict02):
        for i in list01:
            print(i)
            sockfd.send("WJ", dict03[i])
            data, addr = sockfd.recv()
            if data == "None":
                dict02[i] -= 1
                print(dict02)

    def do_send(self, list01, sockfd, addr01, dict03, msg01):
        data = " ".join(list01)
        sockfd.send(data, addr01)
        msg, addr = sockfd.recv()
        sockfd.send("%s" % msg01, dict03[msg])
        return msg

    def shunshou(self, list01, sockfd, addr01, dict03):
        msg = self.do_send(list01, sockfd, addr01, dict03, "SS")
        value, addr = sockfd.recv()
        sockfd.send(value, addr01)
        value, addr = sockfd.recv()
        sockfd.send(value, dict03[msg])
        value, addr = sockfd.recv()
        sockfd.send(value, addr01)

    def guohe(self, list01, sockfd, addr01, dict03):
        msg = self.do_send(list01, sockfd, addr01, dict03, "GH")
        value, addr = sockfd.recv()
        sockfd.send(value, addr01)
        value, addr = sockfd.recv()
        sockfd.send(value, dict03[msg])

    def juedou(self, list01, sockfd, addr01, dict03, dict02):
        data = " ".join(list01)
        sockfd.send(data, addr01)
        msg, addr = sockfd.recv()
        while True:
            sockfd.send("JD", dict03[msg])
            data, addr = sockfd.recv()
            if abs(int(data)) == 1:
                sockfd.send("JD", addr01)
                data, addr = sockfd.recv()
                if abs(int(data)) == 1:
                    continue
                else:
                    dict02[self.find_play(dict03, list01)] -= 1
                    return
            else:
                dict02[msg] -= 1
                return

    def wugu(self, card_list, sockfd, list01, dict03):
        list02 = [card_list.pop(-1), card_list.pop(-2), card_list.pop(-3), card_list.pop(-4), card_list.pop(-5)]
        list03 = list01.copy()
        list03.insert(0, self.find_play(dict03, list01))
        for i in list03:
            value = " ".join(list02)
            sockfd.send("WG %s" % value, dict03[i])
            data, addr = sockfd.recv()
            list02.remove(data)

    def find_nohp(self, dict02):
        for i in dict02:
            if dict02[i] == 0:
                return i
        return False
