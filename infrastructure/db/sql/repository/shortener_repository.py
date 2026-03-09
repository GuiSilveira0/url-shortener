from app.gateway.shortener_repository_gateway import ShortenerRepositoryGateway
from app.entities.db_models_entity import ShortenedUrls
from infrastructure.db.sql.settings.connection import MySqlConnectionHandler

class ShortenerRepository(ShortenerRepositoryGateway):
    def insert_url(self, original_url: str, short_code: str) -> dict:
        with MySqlConnectionHandler() as db:
            new_url = ShortenedUrls(
                original_url=original_url,
                short_code=short_code
            )
            db.session.add(new_url)
            db.session.commit()
            db.session.refresh(new_url)
            
            return {
                "id": new_url.id,
                "original_url": new_url.original_url,
                "short_code": new_url.short_code,
                "created_at": new_url.created_at
            }
    
    def get_url_by_code(self, short_code: str) -> dict:
        with MySqlConnectionHandler() as db:
            url = db.session.query(ShortenedUrls).filter(ShortenedUrls.short_code == short_code).first()
            
            if not url:
                return None
            
            return {
                "id": url.id,
                "original_url": url.original_url,
                "short_code": url.short_code,
                "created_at": url.created_at
            }
