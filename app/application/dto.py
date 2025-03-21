from typing import List, Optional
from pydantic import BaseModel, Field


class SlideDTO(BaseModel):
    title: str
    description: str
    image: Optional[str] = None


class PresentationDTO(BaseModel):
    slides: List[SlideDTO]


class PromptRequest(BaseModel):
    prompt: str = Field(..., min_length=10, description="User prompt to generate presentation content")


class PresentationResponse(BaseModel):
    file_url: str
    slide_count: int
    message: str = "Presentation generated successfully"


class ErrorResponse(BaseModel):
    error: str
    details: Optional[str] = None 
