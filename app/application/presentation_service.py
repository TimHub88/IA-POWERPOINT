import os
import uuid
from typing import Optional

from ..domain.entities import Presentation
from ..domain.repository import AIContentGenerator, PresentationRepository
from .use_cases import GeneratePresentationUseCase


class PresentationService:
    """Service for generating and managing presentations."""
    
    def __init__(
        self,
        content_generator: AIContentGenerator,
        presentation_repository: PresentationRepository
    ):
        self.content_generator = content_generator
        self.presentation_repository = presentation_repository
    
    async def generate_presentation(self, prompt: str, include_images: bool = True) -> Optional[str]:
        """
        Generate a presentation from a user prompt and save it to a file.
        
        Args:
            prompt: User prompt to generate presentation
            include_images: Whether to include images in the presentation
            
        Returns:
            Path to the saved presentation file or None if generation failed
        """
        # Modifier le prompt basé sur le mode images (pour maintenir la compatibilité)
        modified_prompt = self._prepare_prompt(prompt, include_images)
        
        # Generate presentation content - transmettre également le paramètre include_images
        presentation = await self.content_generator.generate_presentation(modified_prompt, include_images)
        
        if not presentation or not presentation.slides:
            return None
        
        # If images should be disabled, clear any image URLs/keywords
        if not include_images:
            self._remove_image_data(presentation)
        
        # Create a unique filename
        filename = f"presentation_{uuid.uuid4().hex}.pptx"
        
        # Save the presentation
        file_path = await self.presentation_repository.save(presentation, filename)
        
        return file_path
    
    def _prepare_prompt(self, prompt: str, include_images: bool) -> str:
        """
        Prepare the prompt based on whether images should be included.
        
        Args:
            prompt: The original user prompt
            include_images: Whether to include images
            
        Returns:
            Modified prompt
        """
        if include_images:
            # Include instruction to generate keywords for images
            return f"{prompt}\n\nInclude descriptive keywords for each slide to find relevant images."
        else:
            # Include instruction to skip image data
            return f"{prompt}\n\nDo not include keywords or images in the slides, focus only on textual content."
    
    def _remove_image_data(self, presentation: Presentation) -> None:
        """
        Remove image data from slides if images are disabled.
        
        Args:
            presentation: The presentation to modify
        """
        for slide in presentation.slides:
            slide.image = ""
            slide.keywords = [] 