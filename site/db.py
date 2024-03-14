import psycopg2
class Adapter():

    def __init__(self, host, port, sslmode, dbname, schema, user, password, target_session_attrs):
        self.host=host
        self.port=port
        self.sslmode=sslmode
        self.dbname=dbname
        self.user=user
        self.password=password
        self.target_session_attrs=target_session_attrs
        self.schema = schema
        self.__connect()
        
    def __connect(self):
        try:
            self.conn = psycopg2.connect(f"""
                host={self.host}
                port={self.port}
                sslmode={self.sslmode}
                dbname={self.dbname}
                user={self.user}
                password={self.password}
                target_session_attrs={self.target_session_attrs}
            """)
        except:
            print('connection error')
        self.cursor = self.conn.cursor()
        
    def select_by_id(self, table, id):
        request = f"""SELECT * FROM "{self.schema}"."{table}" WHERE id = {id}"""
        self.cursor.execute(request)
        data = self.cursor.fetchall()
        return data

    def update(self, table, request, id):
        request_update = f'UPDATE "{self.schema}"."{table}" SET {request} WHERE id={id}'
        cursor = self.conn.cursor()
        cursor.execute(request_update)
        self.conn.commit()

    def insert(self, table, data):
        request_insert = f"""INSERT INTO "{self.schema}"."{table}" ({",".join(list(data.keys()))}) VALUES ({",".join(list(data.items()))})"""
        self.cursor.execute(request_insert)
        self.conn.commit()

    def insert_batch(self,table,data):
        for row in data:
            for key, value in row.items():
                if isinstance(row[key], int):
                    row[key] = str(row[key])
                elif isinstance(row[key], str):
                    row[key] = f"'{row[key]}'"

        for i in range(len(data)):
            request_insert = f"""INSERT INTO "{self.schema}"."{table}" ("{'","'.join(list(data[i].keys()))}") VALUES ({",".join(list(data[i].values()))})"""
            print(request_insert)
            self.cursor.execute(request_insert)
        self.conn.commit()
    
    def delete_by_id(self,table,id):
        request_delete = f"""DELETE FROM "{self.schema}"."{table}" WHERE id = {id}"""
        self.cursor.execute(request_delete)
        self.conn.commit()
class CSV():
    def __init__(self,csv_path):
        self.file=open(csv_path)
    def get_data_from_csv(self):
        res = []
        arr_keys = self.file.readline().split(',')
        all_data = self.file.readlines()
        for i in range(len(all_data)):
            data = all_data[i].split(',')
            data_row_dict = {arr_keys[j].replace("\n",""): data[j].replace("\n","") for j in range(len(arr_keys))}
            res.append(data_row_dict)
        for j in range(len(res)):
            for k,v in res[j].items():
                try:
                    res[j][k] = int(res[j][k])
                except:
                    pass
        return res

db = Adapter(schema="Blue_project",host="rc1d-9cjee2y71olglqhg.mdb.yandexcloud.net",port="6432",dbname="sch58_db",sslmode="verify-full",user="Admin",password="atdhfkm2024",target_session_attrs="read-write")
csv = CSV(r'C:\Users\Степан\OneDrive\Рабочий стол\Python\Blue_gang\site\users.csv')
data = csv.get_data_from_csv()
print(data)
db.insert_batch(table="users",data=data)

#прошу не запускать потому что сериал переменная в айдишнике