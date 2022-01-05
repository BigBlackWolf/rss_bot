from telegram import Update
from telegram.ext import CallbackContext, ConversationHandler
import logging
from settings import CVV, RSS_URL, SETTINGS
from sqlalchemy.exc import IntegrityError
from jobs import add_resource, set_interval

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)


def error_url_handler(update: Update, context: CallbackContext):
    update.message.reply_text("Wrong URL format, please try again or type /cancel")
    return RSS_URL


def add_url_handler(update: Update, context: CallbackContext):
    user = update.message.from_user
    page = update.message.text
    try:
        add_resource(user.id, user.username, page)
    except IntegrityError:
        update.message.reply_text("Resource already exists")
        return RSS_URL
    update.message.reply_text("Resource was successfully added")
    return ConversationHandler.END


def error_setting_interval(update: Update, context: CallbackContext):
    user = update.message.from_user
    logging.info(f"User {user.first_name}")
    update.message.reply_text("Wrong interval, please try again or type /cancel")
    return SETTINGS


def set_interval_handler(update: Update, context: CallbackContext):
    user = update.message.from_user
    interval = int(update.message.text)

    try:
        set_interval(user.id, interval)
    except ValueError as e:
        update.message.reply_text(str(e))
        return SETTINGS
    update.message.reply_text("Interval was successfully set")
    return ConversationHandler.END


def card_number(update: Update, context: CallbackContext):
    user = update.message.from_user
    logger.info(f"Card number of {user.first_name}: {update.message.text}")
    update.message.reply_text("Thanks for your card, dude. Now your cvv")
    return CVV


def skip_card_number(update: Update, context: CallbackContext):
    user = update.message.from_user
    logger.info(f"User {user.first_name} did not send a card number.")
    update.message.reply_text("Well, ok but cvv enter...")
    return CVV
