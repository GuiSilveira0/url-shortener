from app.controller.shortener_controller import router, shortner_usecase
from fastapi import FastAPI, HTTPException, status
from fastapi.responses import RedirectResponse

app = FastAPI(title="URL Shortener")

app.include_router(router)

@app.get("/")
def health_check():
    return {"status": "ok"}

@app.get("/{short_code}")
def redirect_to_url(short_code: str):
    try:
        original_url = shortner_usecase.get_original_url(short_code)
        
        if not original_url:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="URL não encontrada"
            )
        
        return RedirectResponse(url=original_url, status_code=status.HTTP_307_TEMPORARY_REDIRECT)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao buscar URL: {e}"
        )