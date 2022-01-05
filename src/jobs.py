import feedparser
from telegram import Bot
from datetime import datetime, timedelta
import time

from models import Session, User, Resource, Article
from settings import TG_TOKEN, scheduler, TZ
from utils import clean_text

# Some kind of magic with ssl
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

bot = Bot(TG_TOKEN)


def parse(resource: str, interval: int) -> list:
    data = feedparser.parse(resource)
    articles = []
    for entry in data.entries:
        published = datetime.fromtimestamp(time.mktime(entry.published_parsed))
        published = TZ.localize(published)
        corner_time = datetime.now(TZ) - timedelta(days=interval)
        if published < corner_time:
            break
        article = {
            "title": entry.title,
            "link": entry.link,
            "published": published,
            "summary": clean_text(entry.summary)[:200] + "...",
        }
        articles.append(article)
    return articles


def store_articles(resource_id: int, articles: list) -> None:
    article_objs = []
    for article in articles:
        article_obj = Article(
            link=article["link"],
            title=article["title"],
            published=article["published"],
            summary=article["summary"],
            resource_id=resource_id
        )
        article_objs.append(article_obj)
    with Session.begin() as session:
        session.bulk_save_objects(article_objs)


def send_articles(user_id: int, articles: list) -> None:
    for article in articles:
        date = article['published'].strftime("%m %B %Y %H:%M")
        message = f"{article['title']}\n" \
                  f"{date}\n" \
                  f"{article['summary']}\n" \
                  f"{article['link']}"
        bot.send_message(user_id, text=message, disable_web_page_preview=True)


def get_news(user_id: int, interval: int) -> None:
    with Session.begin() as session:
        resources = session.query(Resource.id, Resource.link).filter_by(user_id=user_id).all()
    resources_articles = {i[1]: None for i in resources}
    for resource_id, link in resources:
        resources_articles[link] = parse(link, interval)
        store_articles(resource_id, resources_articles[link])
        send_articles(user_id, resources_articles[link])


def init_user(user_id: int, username: str) -> None:
    with Session.begin() as session:
        user = session.query(User).get(user_id)
        if user is None:
            user = User(id=user_id, username=username)
            session.add(user)


def add_resource(user_id: int, username: str, page: str) -> None:
    with Session.begin() as session:
        user = session.query(User).get(user_id)
        if user is None:
            user = User(id=user_id, username=username)
            session.add(user)
            session.flush()
        resource = Resource(link=page, user_id=user.id)
        session.add(resource)


def set_interval(user_id: int, interval: int) -> None:
    with Session.begin() as session:
        user = session.query(User).get(user_id)
        user.interval = interval
        session.commit()
    scheduler.add_job(
        get_news,
        'interval',
        id=f"interval_{user_id}",
        hours=interval,
        replace_existing=True,
        args=[user_id, interval],
    )
