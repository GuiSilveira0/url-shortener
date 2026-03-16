from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

class AnalyticsRequest(BaseModel):
    short_code: str = Field(..., description="Código curto do link acessado")
    ip_address: Optional[str] = Field(None, description="Endereço IP do visitante")
    user_agent: Optional[str] = Field(None, description="User Agent do navegador")
    referrer: Optional[str] = Field(None, description="URL de origem do acesso")

class AnalyticsResponse(BaseModel):
    id: int
    short_code: str
    accessed_at: datetime
    ip_address: Optional[str]
    country: Optional[str]
    city: Optional[str]
    device_type: Optional[str]
    os: Optional[str]
    browser: Optional[str]
    referrer: Optional[str]

class StatsBasicResponse(BaseModel):
    short_code: str
    total_clicks: int
    unique_clicks: int
    first_access: Optional[datetime]
    last_access: Optional[datetime]

class StatsDetailedResponse(BaseModel):
    short_code: str
    total_clicks: int
    unique_clicks: int
    first_access: Optional[datetime]
    last_access: Optional[datetime]
    top_countries: list
    device_distribution: dict
    browser_distribution: list
    top_referrers: list

class ClicksByPeriodResponse(BaseModel):
    date: str
    clicks: int
    unique_visitors: int

class CountryStatsResponse(BaseModel):
    country: str
    clicks: int
    unique_visitors: int

class DeviceStatsResponse(BaseModel):
    device_type: str
    clicks: int
    percentage: float

class BrowserStatsResponse(BaseModel):
    browser: str
    clicks: int

class ReferrerStatsResponse(BaseModel):
    referrer: str
    clicks: int

class RealtimeStatsResponse(BaseModel):
    short_code: str
    total_clicks: int
    unique_visitors: int
    countries: dict
    devices: dict
    browsers: dict
    daily_clicks: dict
