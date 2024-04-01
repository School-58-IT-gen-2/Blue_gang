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

    def task1(self): 
        request = """SELECT c."id", c."Name", c."Crew", c."Captain", COALESCE(CAST(p."id" AS text), 'unknown') AS "Location" FROM "Galactic Empire"."Cruisers" c LEFT JOIN "Galactic Empire"."Planets" p ON SPLIT_PART("Location", ' ', 1) = p."Name" WHERE c."Crew" <= 200 AND c."Captain" LIKE 'L%' ORDER BY id ASC """
        self.cursor.execute(request)
        data = self.cursor.fetchall()
        return data
db = Adapter(schema="Blue_project",host="rc1d-9cjee2y71olglqhg.mdb.yandexcloud.net",port="6432",dbname="sch58_db",sslmode="verify-full",user="Admin",password="atdhfkm2024",target_session_attrs="read-write")
print(db.task1())