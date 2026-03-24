from datetime import datetime
from typing import List, Optional

from sqlalchemy import func, cast, Date
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
                result = db.session.query(
                    func.count(UrlAnalytics.id).label("total_clicks"),
                    func.count(func.distinct(UrlAnalytics.ip_address)).label("unique_clicks"),
                    func.min(UrlAnalytics.accessed_at).label("first_access"),
                    func.max(UrlAnalytics.accessed_at).label("last_access")
                ).filter(
                    UrlAnalytics.short_code == short_code
                ).first()

                if not result or result.total_clicks == 0:
                    return None

                return {
                    "total_clicks": result.total_clicks,
                    "unique_clicks": result.unique_clicks,
                    "first_access": result.first_access.isoformat() if result.first_access else None,
                    "last_access": result.last_access.isoformat() if result.last_access else None
                }
            except SQLAlchemyError as e:
                raise Exception(f"Erro ao buscar resumo de stats: {str(e)}")

    def get_clicks_by_period(self, short_code: str, start_date: str, end_date: str) -> List[dict]:
        with MySqlConnectionHandler() as db:
            try:
                results = db.session.query(
                    cast(UrlAnalytics.accessed_at, Date).label("date"),
                    func.count(UrlAnalytics.id).label("clicks")
                ).filter(
                    UrlAnalytics.short_code == short_code,
                    cast(UrlAnalytics.accessed_at, Date) >= start_date,
                    cast(UrlAnalytics.accessed_at, Date) <= end_date
                ).group_by(
                    cast(UrlAnalytics.accessed_at, Date)
                ).order_by(
                    cast(UrlAnalytics.accessed_at, Date)
                ).all()

                return [{"date": str(r.date), "clicks": r.clicks} for r in results]
            except SQLAlchemyError as e:
                raise Exception(f"Erro ao buscar cliques por período: {str(e)}")

    def get_top_countries(self, short_code: str, limit: int = 10) -> List[dict]:
        with MySqlConnectionHandler() as db:
            try:
                results = db.session.query(
                    UrlAnalytics.country,
                    func.count(UrlAnalytics.id).label("clicks")
                ).filter(
                    UrlAnalytics.short_code == short_code,
                    UrlAnalytics.country.isnot(None)
                ).group_by(
                    UrlAnalytics.country
                ).order_by(
                    func.count(UrlAnalytics.id).desc()
                ).limit(limit).all()

                return [{"country": r.country, "clicks": r.clicks} for r in results]
            except SQLAlchemyError as e:
                raise Exception(f"Erro ao buscar top países: {str(e)}")

    def get_device_distribution(self, short_code: str) -> List[dict]:
        with MySqlConnectionHandler() as db:
            try:
                results = db.session.query(
                    UrlAnalytics.device_type,
                    func.count(UrlAnalytics.id).label("clicks")
                ).filter(
                    UrlAnalytics.short_code == short_code,
                    UrlAnalytics.device_type.isnot(None)
                ).group_by(
                    UrlAnalytics.device_type
                ).order_by(
                    func.count(UrlAnalytics.id).desc()
                ).all()

                return [{"device": r.device_type, "clicks": r.clicks} for r in results]
            except SQLAlchemyError as e:
                raise Exception(f"Erro ao buscar distribuição de dispositivos: {str(e)}")

    def get_browser_distribution(self, short_code: str) -> List[dict]:
        with MySqlConnectionHandler() as db:
            try:
                results = db.session.query(
                    UrlAnalytics.browser,
                    func.count(UrlAnalytics.id).label("clicks")
                ).filter(
                    UrlAnalytics.short_code == short_code,
                    UrlAnalytics.browser.isnot(None)
                ).group_by(
                    UrlAnalytics.browser
                ).order_by(
                    func.count(UrlAnalytics.id).desc()
                ).all()

                return [{"browser": r.browser, "clicks": r.clicks} for r in results]
            except SQLAlchemyError as e:
                raise Exception(f"Erro ao buscar distribuição de navegadores: {str(e)}")

