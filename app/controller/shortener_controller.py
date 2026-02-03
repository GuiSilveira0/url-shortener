from app.entities.shortener_entity import CreateUrlRequest, UrlResponse
from app.usecase.shortener_usecase import ShortenerUsecase
from fastapi import APIRouter, Depends, HTTPException, status

router = APIRouter(prefix="/api/v1", tags=["URL Shortener"])

shortner_usecase = ShortenerUsecase()

get_usecase = lambda: shortner_usecase

@router.post(
    "/shorten", 
    response_model=UrlResponse, 
    status_code=status.HTTP_201_CREATED,
    summary="Encurta uma URL",
    description="Recebe uma URL longa e retorna uma URL curta gerada automaticamente."
)
def create_short_url(
    request: CreateUrlRequest, 
    usecase: ShortenerUsecase = Depends(get_usecase)
):
    """
    Endpoint para criar uma nova URL curta.
    """
    try:
        short_code = usecase.generate_short_code()
        full_short_url = f"http://localhost:8000/{short_code}"
        
        return UrlResponse(
            original_url=request.url,
            short_code=short_code,
            short_url=full_short_url
        )
        
    except ValueError as ve:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(ve)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno ao processar a URL."
        )