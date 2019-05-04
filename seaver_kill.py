class ServerKill:
    def __init__(self):
        self.p1_dict = {"p2": 1, "p3": 2, "p4": 2, "p5": 1}
        self.p2_dict = {"p1": 1, "p3": 1, "p4": 2, "p5": 2}
        self.p3_dict = {"p1": 2, "p2": 1, "p4": 1, "p5": 2}
        self.p4_dict = {"p2": 2, "p3": 1, "p1": 2, "p5": 1}
        self.p5_dict = {"p2": 2, "p3": 2, "p4": 1, "p1": 1}
        self.dict02 = {}
        self.dict01 = self.dict02.copy()

    def do_kill(self, id, sockfd, addr, value, dict01, list01,do_hp):
        print(value)
        if abs(int(value[1])) == 1 or abs(int(value[1])) == 16:
            data = self.get_where(id, int(value[2]), list01, sockfd, dict01)
            msg = self.return_msg(sockfd, data, addr)
            value = " ".join(value)
            self.kill_player(value, sockfd, msg, dict01)
        elif abs(int(value[1])) == 20:
            data = " ".join(list01)
            value = " ".join(value)
            self.fangtian(sockfd, data, addr, value, dict01)
        else:
            data = " ".join(list01)
            value = " ".join(value)
            msg = self.return_msg(sockfd, data, addr)
            self.choose_player(value, dict01, msg, sockfd, addr)
        i = self.no_hp()
        if i:
            do_hp(i)
        else:
            return 

    def choose_player(self, value, dict01, msg, sockfd, addr):
        data = value.split(" ")
        if 17 <= abs(int(data[1])) <= 18 or abs(int(data[1])) == 21 or abs(int(data[1])) == 29:
            self.kill_player(value, sockfd, msg, dict01)
        elif abs(int(data[1])) == 19:
            self.guanshi(data, sockfd, msg, dict01, addr)
        elif abs(int(data[1])) == 22:
            self.qinglong(value, sockfd, msg, dict01, addr)

    def get_where(self, id, number, list01, sockfd, dict02):
        list02 = []
        dict01 = eval("self.%s_dict" % id)
        self.do_where(dict01, list01, sockfd, dict02)
        for i in dict01:
            if dict01[i] <= number:
                list02.append(i)
        data = " ".join(list02)
        return data

    def do_where(self, dis_dict, list01, sockfd, dict01):
        for i in list01:
            sockfd.send("A", dict01[i])
            data, addr = sockfd.recv()
            if data == "True":
                dis_dict[i] += 1

    def return_msg(self, sockfd, data, addr):
        sockfd.send(data, addr)
        data, addr = sockfd.recv()
        return data

    def kill_player(self, value, sockfd, id, dict01):
        print(value)
        print(dict01, id, dict01[id])
        sockfd.send(value, dict01[id])
        data, addr = sockfd.recv()
        if data == "None":
            self.dict02[id] -= 1
            print(self.dict02)

    def guanshi(self, value, sockfd, id, dict01, addr01):
        data = " ".join(value)
        sockfd.send(data, dict01[id])
        data, addr = sockfd.recv()
        if data == "None":
            self.dict02[id] -= 1
            sockfd.send(data, addr01)
            data, addr = sockfd.recv()
            print(data)
        else:
            sockfd.send(data, addr01)
            data, addr = sockfd.recv()
            if data == "True":
                self.dict02[id] -= 1
            else:
                print(data)

    def fangtian(self, sockfd, data, addr, value, dict01):
        sockfd.send(data, addr)
        data, addr = sockfd.recv()
        list01 = data.split(" ")
        for i in list01:
            self.kill_player(value, sockfd, i, dict01)

    def qinglong(self, value, sockfd, id, dict01, addr01):
        while True:
            sockfd.send(value, dict01[id])
            data, addr = sockfd.recv()
            if data == "None":
                self.dict02[id] -= 1
                sockfd.send(data, addr01)
                data, addr = sockfd.recv()
                print(data)
                return
            else:
                sockfd.send(data, addr01)
                data, addr = sockfd.recv()
                if data == "None":
                    return
                else:
                    value = data

    def no_hp(self):
        for i in self.dict02:
            if self.dict02[i] <= 0:
                return i
        return False
