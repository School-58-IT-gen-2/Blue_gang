from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Функция для отправки сообщения
def send_message(update: Update, context: CallbackContext) -> None:
    chat_id = update.message.chat_id
    context.bot.send_message(chat_id=chat_id, text="Привет! Введите ваш ответ.")

# Функция для получения ответа от пользователя
def get_response(update: Update, context: CallbackContext) -> None:
    user_response = update.message.text
    chat_id = update.message.chat_id
    context.bot.send_message(chat_id=chat_id, text=f"Вы ввели: {user_response}")

# Основная функция, которая инициализирует бота и запускает обработчики
def main() -> None:
    # Токен вашего бота
    token = '6829404815:AAFFRQFdZNB0Hke8aty2pd_c_EooZ_S6oC8'
    
    updater = Updater(token, use_context=True)
    dp = updater.dispatcher

    # Добавляем обработчики команд
    dp.add_handler(CommandHandler("start", send_message))

    # Добавляем обработчик текстовых сообщений
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, get_response))

    # Запускаем бота
    updater.start_polling()

    # Запускаем бота в блоке, чтобы скрипт не завершился
    updater.idle()

if __name__ == '__main__':
    main()
