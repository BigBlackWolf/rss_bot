from telegram import Update
from telegram.ext import CallbackContext, ConversationHandler
import logging
from settings import RSS_URL, SETTINGS
from models import INTERVAL_RANGE
from jobs import init_user

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)


def start(update: Update, context: CallbackContext):
    user = update.message.from_user
    try:
        init_user(user.id, user.username)
    except Exception as e:
        logger.error(f"User: {user.username} ({user.id}) has problems with init")
    finally:
        update.message.reply_text("I'm a rss bot! To start type /add_resource to add new RSS page")


def setting_command(update: Update, context: CallbackContext):
    user = update.message.from_user
    logging.info(f"User {user.first_name}")
    update.message.reply_text(f"Set the interval (in hours) to send you updates. Possible values: {INTERVAL_RANGE}")
    return SETTINGS


def cancel(update: Update, context: CallbackContext):
    user = update.message.from_user
    logger.info(f"User {user.first_name} canceled the conversation.")
    update.message.reply_text("Bye! I hope we can talk again some day.")
    return ConversationHandler.END


def add_resource_handler(update: Update, context: CallbackContext):
    update.message.reply_text("Enter RSS web page")
    return RSS_URL

