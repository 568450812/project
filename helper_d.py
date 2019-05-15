"""
sql　语句
"""

from helper_2 import *


# from member import *


class MenberManage:
    def __init__(self):
        self.mysql = Helper()
        self.mysql.open_mysql()  # 连接数据库

    def __del__(self):
        self.mysql.close_mysql()  # 关闭数据库


    # 根据编号查询密码
    def select_passwd(self, id, passwd):
        value = "select passwd from members where id = '%s'" % id
        result = self.mysql.select(value)
        try:
            if passwd in result[0]:
                return True
            else:
                return False
        except Exception:
            print("输入信息有误")

    #　根据武将编号选择武将类
    def select_hero(self,id):
        value = "select * from hero where id = '%s'"%id
        result = self.mysql.select(value)
        return result[0][1],result[0][2]


if __name__ == "__main__":
    id = "6"
    s = MenberManage()
    a,b = s.select_hero(id)
    print(a)
    print(b)





