from pydantic import BaseModel, HttpUrl, Field

class CreateUrlRequest(BaseModel):
    url: HttpUrl = Field(..., description="A URL longa que será encurtada")

class UrlResponse(BaseModel):
    original_url: str
    short_code: str
    short_url: str

class ErrorResponse(BaseModel):
    detail: str