import feedparser
from settings import ITC_URL
import telegram


def main():
    data = feedparser.parse(ITC_URL)
    for entry in data.entries:
        link = entry.link
        title = entry.title
        published = entry.published
        tags = entry.tags
        for tag in tags:
            tag_name = tag.term
        summary = entry.summary


if __name__ == "__main__":
    main()
    # telegram.Bot.send_message(chat_id=383239642, text="Hey")
