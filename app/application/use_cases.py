import os
import uuid
from typing import Optional

from ..domain.entities import Presentation
from ..domain.repository import AIContentGenerator, PresentationRepository


class GeneratePresentationUseCase:
    def __init__(
        self,
        content_generator: AIContentGenerator,
        presentation_repository: PresentationRepository
    ):
        self.content_generator = content_generator
        self.presentation_repository = presentation_repository

    async def execute(self, prompt: str) -> Optional[str]:
        """
        Generate a presentation from a user prompt and save it to a file.
        
        Args:
            prompt: User prompt to generate presentation
            
        Returns:
            Path to the saved presentation file or None if generation failed
        """
        # Generate presentation content
        presentation = await self.content_generator.generate_presentation(prompt)
        
        if not presentation or not presentation.slides:
            return None
        
        # Create a unique filename
        filename = f"presentation_{uuid.uuid4().hex}.pptx"
        
        # Save the presentation
        file_path = await self.presentation_repository.save(presentation, filename)
        
        return file_path