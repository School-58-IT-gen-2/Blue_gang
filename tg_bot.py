import json

import logging


from telegram import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove, Update, WebAppInfo

from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters


# Enable logging

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

        "Please press the button to start",

        reply_markup=ReplyKeyboardMarkup.from_button(

            KeyboardButton(

                text="Start the game",

                web_app=WebAppInfo(url="https://chess.projectalpha.ru/game"),

            )

        ),

    )



# Handle incoming WebAppData

async def web_app_data(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

    """Print the received data and remove the button."""

    # Here we use `json.loads`, since the WebApp sends the data JSON serialized string

    # (see webappbot.html)

    data = json.loads(update.effective_message.web_app_data.data)

    await update.message.reply_html(

        text=(

            f"You selected the color with the HEX value <code>{data['hex']}</code>. The "

            f"corresponding RGB value is <code>{tuple(data['rgb'].values())}</code>."

        ),

        reply_markup=ReplyKeyboardRemove(),

    )



def main() -> None:

    """Start the bot."""

    # Create the Application and pass it your bot's token.

    application = Application.builder().token("6658441431:AAHIr7viLVGtylMQSBTN0rlzRt05nLW5m50").build()


    application.add_handler(CommandHandler("start", start))

    application.add_handler(MessageHandler(filters.StatusUpdate.WEB_APP_DATA, web_app_data))


    # Run the bot until the user presses Ctrl-C

    application.run_polling(allowed_updates=Update.ALL_TYPES)



if __name__ == "__main__":

    main()