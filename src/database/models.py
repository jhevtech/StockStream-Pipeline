from sqlalchemy import Column, Float, Integer, BigInteger, String, DateTime, Text, Index, UniqueConstraint, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class StockPrice(Base):
    __tablename__ = 'stock_prices'

    id = Column(Integer, primary_key=True, autoincrement=True)
    ticker = Column(String(10), nullable=False)
    timestamp = Column(DateTime, nullable=False)
    open = Column(Float)
    high = Column(Float)
    low = Column(Float)
    close = Column(Float)
    volume = Column(BigInteger)
    created_at = Column(DateTime, default=datetime.utcnow)

    __table_args__ = (
        UniqueConstraint('ticker', 'timestamp', name='uix_ticker_timestamp'),
        Index('idx_ticker_timestamp', 'ticker', 'timestamp'),
    )

class NewsArticle(Base):
    __tablename__ = 'news_article'

    id = Column(Integer, primary_key=True, autoincrement=True)
    ticker = Column(String(10), nullable=False)
    title = Column(String(500), nullable=False)
    source = Column(String(100))
    published_at = Column(DateTime, nullable=False)
    url = Column(Text)
    content = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

    __table_args__ = (
        Index('idx_ticker_published', 'ticker', 'published_at'),
        UniqueConstraint('url', name='uix_url'),
    )

class SentinmentScore(Base):
    __tablename__ = 'sentiment_scores'

    id = Column(Integer, primary_key=True, autoincrement=True)
    article_id = Column(Integer, ForeignKey('news_article.id'), nullable=False)
    ticker = Column(String(10), nullable=False)
    sentiment_score = Column(Float) #compound score from vader
    positive = Column(Float)
    negative = Column(Float)
    neutral = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)


class TechnicalIndicator(Base):
    __tablename__ = 'technical_indicators'

    id = Column(Integer, primary_key=True, autoincrement=True)
    ticker = Column(String(10), nullable=False)
    timestamp = Column(DateTime, nullable=False)
    ma_5 = Column(Float)
    ma_20 = Column(Float)
    volatility_5d = Column(Float)
    rsi = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)

    __table_args__ = (
        UniqueConstraint('ticker', 'timestamp', name='uix_tech_ticker_timestamp'),
        Index('idx_tech_ticker_timestamp', 'ticker', 'timestamp'),

    )

