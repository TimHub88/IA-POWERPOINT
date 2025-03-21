from abc import ABC, abstractmethod
from typing import Optional
from .entities import Presentation


class PresentationRepository(ABC):
    @abstractmethod
    async def save(self, presentation: Presentation, filename: str) -> str:
        """
        Save the presentation to a file and return the file path.
        """
        pass


class AIContentGenerator(ABC):
    @abstractmethod
    async def generate_presentation(self, prompt: str, include_images: bool = True) -> Optional[Presentation]:
        """
        Generate a presentation from a user prompt.
        
        Args:
            prompt: The user prompt
            include_images: Whether to include images in the presentation
            
        Returns:
            A Presentation object or None if generation failed
        """
        pass 
