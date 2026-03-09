from typing import Optional
import datetime

from sqlalchemy import DateTime, Integer, PrimaryKeyConstraint, String, Text, UniqueConstraint, text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    pass


class ShortenedUrls(Base):
    __tablename__ = 'shortened_urls'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='shortened_urls_pkey'),
        UniqueConstraint('short_code', name='shortened_urls_short_code_key')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    original_url: Mapped[str] = mapped_column(Text, nullable=False)
    short_code: Mapped[str] = mapped_column(String(10), nullable=False)
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'))
