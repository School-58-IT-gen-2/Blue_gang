import json
import logging
from telegram import (
    KeyboardButton,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
    Update,
    WebAppInfo,
)
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        reply_markup=ReplyKeyboardMarkup.from_button(
            KeyboardButton(
                text="Start the game",
                web_app=WebAppInfo(url="https://chess.projectalpha.ru/game"),
            )
        ),
    )


async def web_app_data(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    data = json.loads(update.effective_message.web_app_data.data)
    await update.message.reply_html(
        text=(
            f"You selected the color with the HEX value <code>{data['hex']}</code>. The "
            f"corresponding RGB value is <code>{tuple(data['rgb'].values())}</code>."
        ),
        reply_markup=ReplyKeyboardRemove(),
    )

def main() -> None:
    application = (
        Application.builder()
        .token("6658441431:AAHIr7viLVGtylMQSBTN0rlzRt05nLW5m50")
        .build()
    )
    application.add_handler(CommandHandler("start", start))
    application.add_handler(
        MessageHandler(filters.StatusUpdate.WEB_APP_DATA, web_app_data)
    )
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
