from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import JSONResponse, FileResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import os

from ..application.dto import PromptRequest, PresentationResponse, ErrorResponse
from ..application.use_cases import GeneratePresentationUseCase
from ..domain.repository import AIContentGenerator, PresentationRepository
from ..infrastructure.deepseek_client import DeepseekClient
from ..infrastructure.pptx_generator import PPTXGenerator

router = APIRouter()
templates = Jinja2Templates(directory="templates")


def get_content_generator() -> AIContentGenerator:
    return DeepseekClient()


def get_presentation_repository() -> PresentationRepository:
    return PPTXGenerator()


def get_generate_presentation_use_case(
    content_generator: AIContentGenerator = Depends(get_content_generator),
    presentation_repository: PresentationRepository = Depends(get_presentation_repository)
) -> GeneratePresentationUseCase:
    return GeneratePresentationUseCase(content_generator, presentation_repository)


@router.get("/")
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@router.post("/generate", response_model=PresentationResponse, responses={400: {"model": ErrorResponse}, 500: {"model": ErrorResponse}})
async def generate_presentation(
    prompt_request: PromptRequest,
    use_case: GeneratePresentationUseCase = Depends(get_generate_presentation_use_case)
):
    try:
        file_path = await use_case.execute(prompt_request.prompt)
        
        if not file_path:
            raise HTTPException(
                status_code=500,
                detail={"error": "Failed to generate presentation", "details": "Could not generate content from prompt"}
            )
        
        # Count slides (we could use the domain model but this is more direct)
        # The file path is relative to the static folder
        full_path = os.path.join("static", file_path)
        if not os.path.exists(full_path):
            raise HTTPException(
                status_code=500,
                detail={"error": "Failed to save presentation", "details": "Generated file not found"}
            )
        
        # We'll use a simple approximation for slide count
        # In a real application, we would get this from the actual object
        slide_count = len(prompt_request.prompt.split("."))
        
        # Ensure slide count is at least 1
        slide_count = max(1, min(slide_count, 20))
        
        return PresentationResponse(
            file_url=f"/static/{file_path}",
            slide_count=slide_count
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={"error": "An error occurred", "details": str(e)}
        )


@router.get("/download/{filename}")
async def download_presentation(filename: str):
    file_path = os.path.join("static/presentations", filename)
    
    if not os.path.exists(file_path):
        raise HTTPException(
            status_code=404,
            detail={"error": "File not found", "details": "The requested presentation does not exist"}
        )
    
    return FileResponse(file_path, filename=filename) 
