from datetime import datetime
from app.controller.shortener_controller import router, shortner_usecase
from app.controller.analytics_controller import router as analytics_router
from app.usecase.analytics_usecase import AnalyticsUsecase
from fastapi import FastAPI, HTTPException, status, Request, BackgroundTasks
from fastapi.responses import RedirectResponse
from infrastructure.db.sql.repository.analytics_repository import AnalyticsRepository
from infrastructure.db.redis.repository.analytics_redis_repository import AnalyticsRedisRepository
from infrastructure.services.ipapi_service import IPAPIService
from infrastructure.services.user_agent_service import UserAgentService

app = FastAPI(title="URL Shortener")

app.include_router(router)
app.include_router(analytics_router)

analytics_usecase = AnalyticsUsecase(
    analytics_repository=AnalyticsRepository(),
    analytics_redis_repository=AnalyticsRedisRepository()
)

geoip_service = IPAPIService()
user_agent_service = UserAgentService()

@app.get("/")
def health_check():
    return {"status": "ok"}

def track_access_background(analytics_data: dict):
    try:
        analytics_usecase.track_access(analytics_data)
    except Exception as e:
        print(f"Erro ao processar analytics: {e}")

@app.get("/{short_code}")
async def redirect_to_url(short_code: str, request: Request, background_tasks: BackgroundTasks):
    try:
        ip_address = request.headers.get("x-forwarded-for", "").split(",")[0].strip() or request.client.host
        user_agent_string = request.headers.get("user-agent")
        
        location = geoip_service.get_location(ip_address)
        user_agent_data = user_agent_service.parse_user_agent(user_agent_string)
        
        analytics_data = {
            "short_code": short_code,
            "ip_address": ip_address,
            "user_agent": user_agent_string,
            "referrer": request.headers.get("referer"),
            "accessed_at": datetime.now(),
            "country": location.get("country"),
            "city": location.get("city"),
            "device_type": user_agent_data.get("device_type"),
            "os": user_agent_data.get("os"),
            "browser": user_agent_data.get("browser")
        }
        
        original_url = shortner_usecase.get_original_url(short_code)
        
        if not original_url:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="URL não encontrada"
            )
        
        background_tasks.add_task(track_access_background, analytics_data)
        
        return RedirectResponse(url=original_url, status_code=status.HTTP_307_TEMPORARY_REDIRECT)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao buscar URL: {e}"
        )