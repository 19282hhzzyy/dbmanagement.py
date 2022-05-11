import sqlite3


class DBData:
    def __init__(self, user_name, fingerprint, user_password, permissio, user_type):
        self.user_id = None
        self.user_name = user_name
        self.fingerprint = fingerprint
        self.user_password = user_password
        self.permissio = permissio
        self.user_type = user_type


class DaseData:
    def __init__(self):
        # 当前正在处理的数据库
        self.conn = None
        self.cursor = None
        self.database_dic = {}
        self.database_name = None

    def get_database_dic(self):
        return self.database_dic

    def get_database_name(self):
        return self.database_name

    # 创建新数据库
    def new_database(self, path):
        self.conn = sqlite3.connect(path)
        self.cursor = self.conn.cursor()
        sql = "create table if not exists userdb(" \
              "user_id integer primary key," \
              "user_name text unique ," \
              "fingerprint text," \
              "user_password text," \
              "permissio text," \
              "user_type text)"

        self.cursor.execute(sql)
        self.database_name = path.split('/')[-1][:-3]
        self.database_dic[self.database_name] = []

    # 打开数据库并获得当前数据库全部数据
    def open_dase(self, path):
        self.conn = sqlite3.connect(path)
        self.cursor = self.conn.cursor()
        sql = """select * from userdb"""
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        self.database_name = path.split('/')[-1][:-3]
        self.database_dic[self.database_name] = []
        for i in range(len(result)):
            d = DBData(
                result[i][1],
                result[i][2],
                result[i][3],
                result[i][4],
                result[i][5]
            )
            d.user_id = result[i][0]
            self.database_dic[self.database_name].append(d)

    # 往数据库中添加数据
    def add_data(self, d: DBData):
        try:
            self.cursor.execute("insert into userdb values(?,?,?,?,?,?)",
                                (None, d.user_name, d.fingerprint, d.user_password, d.permissio, d.user_type))
            self.conn.commit()
            self.update_date()
            return 1
        except:
            return 0

    # 编辑数据
    def edit_data(self, d: DBData):
        # try:
        sql = f"""update userdb set user_name='{d.user_name}',fingerprint='{d.fingerprint}',user_password='{d.user_password}',permissio='{d.permissio}',user_type='{d.user_type}' where user_name='{d.user_name}'"""
        self.cursor.execute(sql)
        self.conn.commit()
        self.update_date()
        # return 1
        # except:
        #     return 0

    # 删除数据
    def del_data(self, user_name):
        # try:
        sql = f"""delete from userdb where user_name = '{user_name}'"""
        self.cursor.execute(sql)
        self.conn.commit()
        self.update_date()

    # 更新数据
    def update_date(self):
        sql = """select * from userdb"""
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        self.database_dic[self.database_name] = []
        for i in range(len(result)):
            d = DBData(
                result[i][1],
                result[i][2],
                result[i][3],
                result[i][4],
                result[i][5]
            )
            d.user_id = result[i][0]
            self.database_dic[self.database_name].append(d)

    def on_save_as(self, new_path):
        target = sqlite3.connect(new_path)
        self.conn.backup(target)
