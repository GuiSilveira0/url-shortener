from app.controller import shortener_controller
from fastapi import FastAPI

app = FastAPI(title="URL Shortener")

app.include_router(shortener_controller)

@app.get("/")
def health_check():
    return {"status": "ok"}