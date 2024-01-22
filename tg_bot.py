import json
import logging

from telegram import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove, Update, WebAppInfo
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters


logging.basicConfig(

    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO

)

# set higher logging level for httpx to avoid all GET and POST requests being logged

logging.getLogger("httpx").setLevel(logging.WARNING)


logger = logging.getLogger(__name__)



# Define a `/start` command handler.

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

    """Send a message with a button that opens a the web app."""

    await update.message.reply_text(

        "Привет! ты в телеграм боте синей команды, нажми на кнопку, чтобы поиграть в самую оригинальную игру",

        reply_markup=ReplyKeyboardMarkup.from_button(

            KeyboardButton(

                text="Начать игру",

                web_app=WebAppInfo(url="https://chess.projectalpha.ru/game"),

            )

        ),

    )


def main() -> None:

    """Start the bot."""

    # Create the Application and pass it your bot's token.

    application = Application.builder().token("6658441431:AAHIr7viLVGtylMQSBTN0rlzRt05nLW5m50").build()


    application.add_handler(CommandHandler("start", start))



    # Run the bot until the user presses Ctrl-C

    application.run_polling(allowed_updates=Update.ALL_TYPES)



if __name__ == "__main__":

    main()