from datetime import date, timedelta
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.entities.analytics_entity import (
    DetailedAnalyticsResponse,
    RealtimeStatsResponse,
    UrlStatsResponse,
)
from app.usecase.analytics_usecase import AnalyticsUsecase
from infrastructure.db.redis.repository.analytics_redis_repository import AnalyticsRedisRepository
from infrastructure.db.sql.repository.analytics_repository import AnalyticsRepository

router = APIRouter(prefix="/api/v1", tags=["Analytics"])

analytics_usecase = AnalyticsUsecase(
    analytics_repository=AnalyticsRepository(),
    analytics_redis_repository=AnalyticsRedisRepository()
)

get_usecase = lambda: analytics_usecase


@router.get(
    "/stats/{short_code}",
    response_model=UrlStatsResponse,
    summary="Estatísticas básicas",
    description="Retorna estatísticas gerais de um link encurtado (dados do PostgreSQL)."
)
def get_basic_stats(
    short_code: str,
    usecase: AnalyticsUsecase = Depends(get_usecase)
):
    try:
        stats = usecase.get_url_statistics(short_code)
        if not stats:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Nenhuma estatística encontrada para este código."
            )
        return UrlStatsResponse(short_code=short_code, **stats)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao buscar estatísticas: {e}"
        )


@router.get(
    "/analytics/{short_code}",
    response_model=DetailedAnalyticsResponse,
    summary="Analytics detalhado",
    description="Retorna analytics detalhado com cliques por dia em um período específico."
)
def get_detailed_analytics(
    short_code: str,
    start_date: Optional[date] = Query(None, description="Data inicial (YYYY-MM-DD)"),
    end_date: Optional[date] = Query(None, description="Data final (YYYY-MM-DD)"),
    usecase: AnalyticsUsecase = Depends(get_usecase)
):
    if not end_date:
        end_date = date.today()
    if not start_date:
        start_date = end_date - timedelta(days=30)

    try:
        result = usecase.get_detailed_analytics(short_code, str(start_date), str(end_date))
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Nenhuma estatística encontrada para este código."
            )
        return DetailedAnalyticsResponse(short_code=short_code, **result)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao buscar analytics detalhado: {e}"
        )


@router.get(
    "/analytics/{short_code}/realtime",
    response_model=RealtimeStatsResponse,
    summary="Estatísticas em tempo real",
    description="Retorna estatísticas em tempo real do Redis (últimos 7 dias)."
)
def get_realtime_stats(
    short_code: str,
    usecase: AnalyticsUsecase = Depends(get_usecase)
):
    try:
        stats = usecase.get_realtime_stats(short_code)
        return RealtimeStatsResponse(short_code=short_code, **stats)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao buscar estatísticas em tempo real: {e}"
        )
