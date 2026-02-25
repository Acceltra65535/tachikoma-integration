import ibkr
import logging
import ipinfo
import pytz

from datetime import datetime
from html import escape
from uuid import uuid4

from telegram import InlineQueryResultArticle, InputTextMessageContent, Update
from telegram.constants import ParseMode
from telegram.ext import Application, CommandHandler, ContextTypes, InlineQueryHandler

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

# Define a few command handlers. These usually take the two arguments update and
# context.
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    await update.message.reply_text("Hi!")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text("Help!")


async def inline_query(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the inline query. This is run when you type: @botusername <query>"""
    #access_token = 'N/A'
    #handler = ipinfo.getHandler(access_token)

    # Specify the Singapore time zone
    tz = pytz.timezone('Asia/Singapore')

    # Get the current time in that specific time zone
    singapore_time = datetime.now(tz)

    # To print only the time in a specific format (e.g., HH:MM:SS)
    formatted_time = singapore_time.strftime("%H:%M:%S")

    query = update.inline_query.query
    #ip_address = query
    #details = handler.getDetails(ip_address)
    ibkr.run_loop()
    ibkr.app.disconnect()

    if not query:  # empty query should not be handled
        return

    results = [

        InlineQueryResultArticle(
            id=str(uuid4()),
            title="IBKR SG FX",
            input_message_content=InputTextMessageContent(
                f"USD 美元/ CNH 离岸人民币 实时: <b>{ibkr.preturn}</b>\n\n新加坡时间: <b>{formatted_time}</b>", parse_mode=ParseMode.HTML
            ),
        )
    ]

    await update.inline_query.answer(results, cache_time = 0)


def main() -> None:
    """Run the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token("N/A").build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))

    # on inline queries - show corresponding inline results
    application.add_handler(InlineQueryHandler(inline_query))

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()