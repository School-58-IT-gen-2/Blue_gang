import psycopg2
class Adapter():

    def __init__(self):
        self.__connect()
        
    def __connect(self):
        try:
            self.conn = psycopg2.connect(f"""
                host=rc1d-9cjee2y71olglqhg.mdb.yandexcloud.net
                port=6432
                sslmode=verify-full
                dbname=sch58_db
                user=Admin
                password=atdhfkm2024
                target_session_attrs=read-write
            """)
        except:
            print('connection error')
        
    def get(self, requeste ,table):
        request = f'SELECT {requeste} FROM "Blue_project"."{table}"'
        cursor = self.conn.cursor()
        cursor.execute(request)
        data = cursor.fetchall()
        return data

    def get_by_id(self, requeste, table, id):
        request = f'SELECT {requeste} FROM "Blue_project"."{table} WHERE id={id}"'
        cursor = self.conn.cursor()
        cursor.execute(request)
        data = cursor.fetchall()
        return data

    def update(self, table, request, id):
        request_update = f'UPDATE "Blue_project"."{table}" SET {request} WHERE id={id}'
        cursor = self.conn.cursor()
        cursor.execute(request_update)
        self.conn.commit()

    def insert(self, table, collumns, values):
        request_insert = f'INSERT INTO "Blue_project"."{table}" ({collumns}) VALUES ({values})'
        cursor = self.conn.cursor()
        cursor.execute(request_insert)
        self.conn.commit()

db = Adapter()
db.update("users",'"username"=\'werwer1\', "password"=\'1234t\' ,"mail" = \'werwer2@wer\', "rating"=15342, created=333333', '1')
#db.insert("users", 'id, "username", "password", "mail", "rating", "created"', "DEFAULT ,\'werwer2\', \'werwer2\', \'werwer2\' , 123, 1233")
print(db.get_all("*",'users'))