from typing import Callable

from fastapi import Depends

from ..application.presentation_service import PresentationService
from ..domain.repository import AIContentGenerator, PresentationRepository
from ..infrastructure.deepseek_client import DeepseekClient
from ..infrastructure.pptx_generator import PPTXGenerator


def get_content_generator() -> AIContentGenerator:
    """Get the AIContentGenerator implementation."""
    return DeepseekClient()


def get_presentation_repository() -> PresentationRepository:
    """Get the PresentationRepository implementation."""
    return PPTXGenerator()


def get_presentation_service(
    content_generator: AIContentGenerator = Depends(get_content_generator),
    presentation_repository: PresentationRepository = Depends(get_presentation_repository)
) -> PresentationService:
    """Get the PresentationService instance."""
    return PresentationService(
        content_generator=content_generator,
        presentation_repository=presentation_repository
    )
