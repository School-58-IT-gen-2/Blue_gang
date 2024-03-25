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
        self.connect()
        
    def connect(self):
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
        return self.conn
        
    def select_sth_by_condition(self, sth, table, condition):
        request = f"""SELECT {sth} FROM "{self.schema}"."{table}" WHERE {condition}"""
        self.cursor.execute(request)
        data = self.cursor.fetchall()
        return data

    def update(self, table, request, id):
        request_update = f'UPDATE "{self.schema}"."{table}" SET {request} WHERE id={id}'
        cursor = self.conn.cursor()
        cursor.execute(request_update)
        self.conn.commit()

    def insert(self, table, columns, values):
        request_insert = f"""INSERT INTO "{self.schema}"."{table}" ({columns}) VALUES ({values})"""
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
            request_insert = f"""INSERT INTO "{self.schema}"."{table}" ({'","'.join(list(data[i].keys()))}) VALUES ("{",".join(list(data[i].values()))}")"""
            print(request_insert)
            self.cursor.execute(request_insert)
        self.conn.commit()
    
    def delete_by_id(self,table,id):
        request_delete = f"""DELETE FROM "{self.schema}"."{table}" WHERE id = {id}"""
        self.cursor.execute(request_delete)
        self.conn.commit()
