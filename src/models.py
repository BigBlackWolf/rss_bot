from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey,
    create_engine,
    UniqueConstraint,
)
from sqlalchemy.dialects.mysql import BLOB, DOUBLE
from sqlalchemy.orm import (
    declarative_base,
    relationship,
    sessionmaker,
    validates,
)
from settings import DB_DSN

Base = declarative_base()
engine = create_engine(DB_DSN, echo=True)
Session = sessionmaker(bind=engine)

INTERVAL_RANGE = (1, 2, 3, 6, 12, 24)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(255))
    interval = Column(Integer)

    resources = relationship("Resource", back_populates='user', cascade="all, delete, delete-orphan")

    @validates('interval')
    def validate_interval(self, key, interval):
        if interval not in INTERVAL_RANGE:
            raise ValueError(f"Interval should be one of {INTERVAL_RANGE}")
        return interval


class Resource(Base):
    __tablename__ = "resources"
    __table_args__ = (UniqueConstraint('user_id', 'link', name='_user_link_uc'),)

    id = Column(Integer, primary_key=True)
    link = Column(String(300), index=True)
    user_id = Column(Integer, ForeignKey('users.id'))

    user = relationship("User", back_populates="resources")
    articles = relationship("Article", back_populates='resource', cascade="all, delete, delete-orphan")


class Article(Base):
    __tablename__ = "articles"

    id = Column(Integer, primary_key=True)
    link = Column(String(300), index=True)
    title = Column(String(200))
    published = Column(DateTime)
    summary = Column(String(205))
    resource_id = Column(Integer, ForeignKey('resources.id'))

    resource = relationship("Resource", back_populates="articles")
#     tags = relationship("Tag", back_populates='article', cascade="all, delete, delete-orphan")
#
#
# class Tag(Base):
#     __tablename__ = "tags"
#
#     id = Column(Integer, primary_key=True)
#     title = Column(String(50), unique=True, index=True)
#     article_id = Column(Integer, ForeignKey('articles.id'))
#
#     article = relationship("Article", back_populates="tags")


class Apscheduler(Base):
    __tablename__ = "apscheduler"

    id = Column(String(191), primary_key=True)
    next_run_time = Column(DOUBLE, index=True)
    job_state = Column(BLOB)


def migrate_all():
    Base.metadata.create_all(engine)


def drop_all():
    Base.metadata.drop_all(engine)
