from typing import Optional
import datetime

from sqlalchemy import DateTime, ForeignKeyConstraint, Index, Integer, PrimaryKeyConstraint, String, Text, UniqueConstraint, text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

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

    url_analytics: Mapped[list['UrlAnalytics']] = relationship('UrlAnalytics', back_populates='shortened_urls')
    url_stats_summary: Mapped['UrlStatsSummary'] = relationship('UrlStatsSummary', uselist=False, back_populates='shortened_urls')


class UrlAnalytics(Base):
    __tablename__ = 'url_analytics'
    __table_args__ = (
        ForeignKeyConstraint(['short_code'], ['shortened_urls.short_code'], ondelete='CASCADE', name='fk_short_code_analytics'),
        PrimaryKeyConstraint('id', name='url_analytics_pkey'),
        Index('idx_analytics_accessed_at', 'accessed_at'),
        Index('idx_analytics_country', 'country'),
        Index('idx_analytics_device_type', 'device_type'),
        Index('idx_analytics_short_code', 'short_code'),
        {'comment': 'Registra cada acesso individual aos links encurtados'}
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    short_code: Mapped[str] = mapped_column(String(10), nullable=False, comment='C�digo curto do link acessado')
    accessed_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'), comment='Data e hora do acesso')
    ip_address: Mapped[Optional[str]] = mapped_column(String(45), comment='Endere�o IP do visitante (pode ser anonimizado)')
    country: Mapped[Optional[str]] = mapped_column(String(100), comment='Pa�s de origem do acesso')
    city: Mapped[Optional[str]] = mapped_column(String(100), comment='Cidade de origem do acesso')
    device_type: Mapped[Optional[str]] = mapped_column(String(50), comment='Tipo de dispositivo (Desktop, Mobile, Tablet)')
    os: Mapped[Optional[str]] = mapped_column(String(50), comment='Sistema operacional do visitante')
    browser: Mapped[Optional[str]] = mapped_column(String(50), comment='Navegador utilizado')
    referrer: Mapped[Optional[str]] = mapped_column(Text, comment='URL de origem do acesso')
    user_agent: Mapped[Optional[str]] = mapped_column(Text, comment='String completa do User Agent')

    shortened_urls: Mapped['ShortenedUrls'] = relationship('ShortenedUrls', back_populates='url_analytics')


class UrlStatsSummary(Base):
    __tablename__ = 'url_stats_summary'
    __table_args__ = (
        ForeignKeyConstraint(['short_code'], ['shortened_urls.short_code'], ondelete='CASCADE', name='fk_short_code_summary'),
        PrimaryKeyConstraint('id', name='url_stats_summary_pkey'),
        UniqueConstraint('short_code', name='url_stats_summary_short_code_key'),
        Index('idx_summary_short_code', 'short_code', unique=True),
        {'comment': 'Estat�sticas agregadas dos links para consultas r�pidas'}
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    short_code: Mapped[str] = mapped_column(String(10), nullable=False, comment='C�digo curto do link')
    total_clicks: Mapped[Optional[int]] = mapped_column(Integer, server_default=text('0'), comment='Total de cliques no link')
    unique_clicks: Mapped[Optional[int]] = mapped_column(Integer, server_default=text('0'), comment='N�mero de visitantes �nicos (IPs distintos)')
    first_access: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, comment='Data e hora do primeiro acesso')
    last_access: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, comment='Data e hora do �ltimo acesso')
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'), comment='�ltima atualiza��o dos dados agregados')

    shortened_urls: Mapped['ShortenedUrls'] = relationship('ShortenedUrls', back_populates='url_stats_summary')
