import psycopg2
class Adapter():

    def __init__(self, host, port, sslmode, dbname, user, password, target_session_attrs):
        
        self.host=host
        self.port=port
        self.sslmode=sslmode
        self.dbname=dbname
        self.user=user
        self.password=password
        self.target_session_attrs=target_session_attrs
        
    def connect(self):
        #try:
        if 1:
            self.conn = psycopg2.connect(f"""
                host={self.host}
                port={self.port}
                sslmode={self.sslmode}
                dbname={self.dbname}
                user={self.user}
                password={self.password}
                target_session_attrs={self.target_session_attrs}
            """)
        #except:
            #print('connection error')

    def select(self, table):
        request = f'SELECT * FROM "Blue_project"."{table}"'
        self.cursor = self.conn.cursor()
        self.cursor.execute(request)
        data = self.cursor.fetchall()
        return data
    
    def update(self, table, request, id):
        request_update = f'UPDATE "Blue_project"."{table}" SET {request} WHERE id={id}'
        self.cursor.execute(request_update)
        self.conn.commit()

    def insert(self, table, collumns, values):
        request_insert = f'INSERT INTO "Blue_project"."{table}" ({collumns}) VALUES ({values})'
        self.cursor.execute(request_insert)

db = Adapter('rc1d-9cjee2y71olglqhg.mdb.yandexcloud.net','6432','verify-full','sch58_db','Admin','atdhfkm2024','read-write')
db.connect()