from datetime import datetime, date
from typing import List, Optional
from sqlalchemy import func
from sqlalchemy.exc import SQLAlchemyError
from app.gateway.analytics_repository_gateway import AnalyticsRepositoryGateway
from infrastructure.db.sql.settings.connection import MySqlConnectionHandler
from app.entities.db_models_entity import UrlAnalytics, UrlStatsSummary

class AnalyticsRepository(AnalyticsRepositoryGateway):
    
    def insert_analytics(self, analytics_data: dict) -> None:
        with MySqlConnectionHandler() as db:
            try:
                new_analytics = UrlAnalytics(
                    short_code=analytics_data.get("short_code"),
                    accessed_at=analytics_data.get("accessed_at", datetime.now()),
                    ip_address=analytics_data.get("ip_address"),
                    country=analytics_data.get("country"),
                    city=analytics_data.get("city"),
                    device_type=analytics_data.get("device_type"),
                    os=analytics_data.get("os"),
                    browser=analytics_data.get("browser"),
                    referrer=analytics_data.get("referrer"),
                    user_agent=analytics_data.get("user_agent")
                )
                
                db.session.add(new_analytics)
                db.session.commit()
            except SQLAlchemyError as e:
                db.session.rollback()
                raise Exception(f"Erro ao salvar analytics: {str(e)}")
    
    def get_stats_summary(self, short_code: str) -> Optional[dict]:
        with MySqlConnectionHandler() as db:
            try:
                summary = db.session.query(UrlStatsSummary).filter(
                    UrlStatsSummary.short_code == short_code
                ).first()
                
                if not summary:
                    return None
                
                return {
                    "short_code": summary.short_code,
                    "total_clicks": summary.total_clicks,
                    "unique_clicks": summary.unique_clicks,
                    "first_access": summary.first_access,
                    "last_access": summary.last_access,
                    "updated_at": summary.updated_at
                }
            except SQLAlchemyError as e:
                raise Exception(f"Erro ao buscar summary: {str(e)}")
    
    def get_clicks_by_period(self, short_code: str, start_date: date, end_date: date) -> List[dict]:
        with MySqlConnectionHandler() as db:
            try:
                results = db.session.query(
                    func.date(UrlAnalytics.accessed_at).label('date'),
                    func.count(UrlAnalytics.id).label('clicks'),
                    func.count(func.distinct(UrlAnalytics.ip_address)).label('unique_visitors')
                ).filter(
                    UrlAnalytics.short_code == short_code,
                    func.date(UrlAnalytics.accessed_at) >= start_date,
                    func.date(UrlAnalytics.accessed_at) <= end_date
                ).group_by(
                    func.date(UrlAnalytics.accessed_at)
                ).order_by(
                    func.date(UrlAnalytics.accessed_at)
                ).all()
                
                return [
                    {
                        "date": str(row.date),
                        "clicks": row.clicks,
                        "unique_visitors": row.unique_visitors
                    }
                    for row in results
                ]
            except SQLAlchemyError as e:
                raise Exception(f"Erro ao buscar cliques por período: {str(e)}")
    
    def get_top_countries(self, short_code: str, limit: int = 10) -> List[dict]:
        with MySqlConnectionHandler() as db:
            try:
                results = db.session.query(
                    UrlAnalytics.country,
                    func.count(UrlAnalytics.id).label('clicks'),
                    func.count(func.distinct(UrlAnalytics.ip_address)).label('unique_visitors')
                ).filter(
                    UrlAnalytics.short_code == short_code,
                    UrlAnalytics.country.isnot(None)
                ).group_by(
                    UrlAnalytics.country
                ).order_by(
                    func.count(UrlAnalytics.id).desc()
                ).limit(limit).all()
                
                return [
                    {
                        "country": row.country,
                        "clicks": row.clicks,
                        "unique_visitors": row.unique_visitors
                    }
                    for row in results
                ]
            except SQLAlchemyError as e:
                raise Exception(f"Erro ao buscar top países: {str(e)}")
    
    def get_device_distribution(self, short_code: str) -> dict:
        with MySqlConnectionHandler() as db:
            try:
                results = db.session.query(
                    UrlAnalytics.device_type,
                    func.count(UrlAnalytics.id).label('clicks')
                ).filter(
                    UrlAnalytics.short_code == short_code,
                    UrlAnalytics.device_type.isnot(None)
                ).group_by(
                    UrlAnalytics.device_type
                ).all()
                
                total = sum(row.clicks for row in results)
                
                return {
                    "devices": [
                        {
                            "device_type": row.device_type,
                            "clicks": row.clicks,
                            "percentage": round((row.clicks / total * 100), 2) if total > 0 else 0
                        }
                        for row in results
                    ],
                    "total": total
                }
            except SQLAlchemyError as e:
                raise Exception(f"Erro ao buscar distribuição de dispositivos: {str(e)}")
    
    def get_browser_distribution(self, short_code: str) -> List[dict]:
        with MySqlConnectionHandler() as db:
            try:
                results = db.session.query(
                    UrlAnalytics.browser,
                    func.count(UrlAnalytics.id).label('clicks')
                ).filter(
                    UrlAnalytics.short_code == short_code,
                    UrlAnalytics.browser.isnot(None)
                ).group_by(
                    UrlAnalytics.browser
                ).order_by(
                    func.count(UrlAnalytics.id).desc()
                ).all()
                
                return [
                    {
                        "browser": row.browser,
                        "clicks": row.clicks
                    }
                    for row in results
                ]
            except SQLAlchemyError as e:
                raise Exception(f"Erro ao buscar distribuição de navegadores: {str(e)}")
    
    def get_top_referrers(self, short_code: str, limit: int = 10) -> List[dict]:
        with MySqlConnectionHandler() as db:
            try:
                results = db.session.query(
                    UrlAnalytics.referrer,
                    func.count(UrlAnalytics.id).label('clicks')
                ).filter(
                    UrlAnalytics.short_code == short_code,
                    UrlAnalytics.referrer.isnot(None),
                    UrlAnalytics.referrer != ''
                ).group_by(
                    UrlAnalytics.referrer
                ).order_by(
                    func.count(UrlAnalytics.id).desc()
                ).limit(limit).all()
                
                return [
                    {
                        "referrer": row.referrer,
                        "clicks": row.clicks
                    }
                    for row in results
                ]
            except SQLAlchemyError as e:
                raise Exception(f"Erro ao buscar top referrers: {str(e)}")
