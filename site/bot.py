from telegram import Update
from telegram.ext import Updater, CommandHandler, filters,MessageHandler, CallbackContext
import psycopg2
import time

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

    def update(self, table, request, where):
        request_update = f'UPDATE "{self.schema}"."{table}" SET {request} WHERE {where} '
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

db = Adapter(schema="Blue_project",host="rc1d-9cjee2y71olglqhg.mdb.yandexcloud.net",port="6432",dbname="sch58_db",sslmode="verify-full",user="Admin",password="atdhfkm2024",target_session_attrs="read-write")

def update_database(update: Update):
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id
    username = update.effective_user.username
    now = int(time.time())
    
    db.cursor.execute("SELECT * FROM user_data WHERE user_id = %s", (user_id))
    existing_user = db.cursor.fetchone()
    
    if existing_user:
        db.update("tg_users",f"updated = {now}",f"user_id = {user_id}")
    else:
        db.insert("tg_users",{"chat_id": chat_id, "user_id": user_id, "username": username, "created": now, "updated": now})
    

# Обработчик команды /start
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Привет! Добро пожаловать!')

    # Записываем данные при первом заходе пользователя в бота
    update_database(update)

# Обработчик всех входящих сообщений
def echo(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(update.message.text)

    # Обновляем данные при каждом контакте с пользователем
    update_database(update)

def main() -> None:
    
    updater = Updater("")
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler('start',start))
    dp.add_handler(MessageHandler(filters.text & ~filters.command, echo))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()


# чёто я нафидил с ботом и не оч работает