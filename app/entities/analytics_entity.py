from typing import List, Optional
from pydantic import BaseModel, Field


class CountryStats(BaseModel):
    country: str = Field(..., description="Nome do país")
    clicks: int = Field(..., description="Quantidade de cliques")


class DeviceStats(BaseModel):
    device: str = Field(..., description="Tipo de dispositivo")
    clicks: int = Field(..., description="Quantidade de cliques")


class BrowserStats(BaseModel):
    browser: str = Field(..., description="Nome do navegador")
    clicks: int = Field(..., description="Quantidade de cliques")


class DailyClicks(BaseModel):
    date: str = Field(..., description="Data no formato YYYY-MM-DD")
    clicks: int = Field(..., description="Quantidade de cliques no dia")


class UrlStatsResponse(BaseModel):
    short_code: str = Field(..., description="Código curto do link")
    total_clicks: int = Field(..., description="Total de cliques")
    unique_clicks: int = Field(..., description="Visitantes únicos")
    first_access: Optional[str] = Field(None, description="Data do primeiro acesso")
    last_access: Optional[str] = Field(None, description="Data do último acesso")
    top_countries: List[CountryStats] = Field(default_factory=list, description="Top países por cliques")
    top_devices: List[DeviceStats] = Field(default_factory=list, description="Distribuição por dispositivo")
    top_browsers: List[BrowserStats] = Field(default_factory=list, description="Distribuição por navegador")


class DetailedAnalyticsResponse(BaseModel):
    short_code: str = Field(..., description="Código curto do link")
    total_clicks: int = Field(..., description="Total de cliques no período")
    unique_clicks: int = Field(..., description="Visitantes únicos no período")
    clicks_by_day: List[DailyClicks] = Field(default_factory=list, description="Cliques por dia")
    top_countries: List[CountryStats] = Field(default_factory=list, description="Top países")
    top_devices: List[DeviceStats] = Field(default_factory=list, description="Distribuição por dispositivo")
    top_browsers: List[BrowserStats] = Field(default_factory=list, description="Distribuição por navegador")


class RealtimeStatsResponse(BaseModel):
    short_code: str = Field(..., description="Código curto do link")
    total_clicks: int = Field(..., description="Total de cliques (cache)")
    unique_clicks: int = Field(..., description="Visitantes únicos (cache)")
    countries: dict = Field(default_factory=dict, description="Cliques por país")
    devices: dict = Field(default_factory=dict, description="Cliques por dispositivo")
    browsers: dict = Field(default_factory=dict, description="Cliques por navegador")
