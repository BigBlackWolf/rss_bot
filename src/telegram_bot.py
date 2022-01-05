from telegram.ext import CommandHandler, Updater, MessageHandler, Filters, ConversationHandler
from settings import TG_TOKEN, RSS_URL, URL_REGEX, CANCEL_REGEX, SETTINGS, scheduler
from handlers import (
    add_url_handler,
    error_url_handler,
    set_interval_handler,
    error_setting_interval,
)
from commands import (
    start,
    cancel,
    add_resource_handler,
    setting_command,
)


class Telegram:
    def __init__(self):
        self.updater = Updater(token=TG_TOKEN, use_context=True)
        self.dispatcher = self.updater.dispatcher
        self.add_handlers()

    def add_handlers(self):
        add_rss = ConversationHandler(
            entry_points=[
                CommandHandler("start", start),
                CommandHandler("add_resource", add_resource_handler)
            ],
            states={
                RSS_URL: [
                    MessageHandler(Filters.regex(URL_REGEX), add_url_handler),
                    MessageHandler(~Filters.regex(CANCEL_REGEX), error_url_handler)
                ],
            },
            fallbacks=[CommandHandler("cancel", cancel)]
        )
        self.dispatcher.add_handler(add_rss)

        settings_handler = ConversationHandler(
            entry_points=[
                CommandHandler("settings", setting_command),
            ],
            states={
                SETTINGS: [
                    MessageHandler(Filters.regex(r"^\d+$"), set_interval_handler),
                    MessageHandler(~Filters.regex(CANCEL_REGEX), error_setting_interval)
                ],
            },
            fallbacks=[CommandHandler("cancel", cancel)]
        )
        self.dispatcher.add_handler(settings_handler)

    def start(self):
        self.updater.start_polling()
        self.updater.job_queue.stop()
        scheduler.start()
        self.updater.idle()


telegram_instance = Telegram()


def main():
    telegram_instance.start()


if __name__ == '__main__':
    main()
