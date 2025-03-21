from typing import List, Optional
from dataclasses import dataclass, field


@dataclass
class Slide:
    """A slide in a presentation."""
    
    title: str
    description: str
    image: Optional[str] = None
    keywords: Optional[List[str]] = None

    def to_dict(self) -> dict:
        """Convert to dictionary representation."""
        return {
            "title": self.title,
            "description": self.description,
            "image": self.image,
            "keywords": self.keywords
        }


@dataclass
class Presentation:
    """A presentation containing multiple slides."""
    
    slides: List[Slide] = field(default_factory=list)
    
    @classmethod
    def create_empty(cls) -> 'Presentation':
        """Create an empty presentation."""
        return cls()
    
    def add_slide(self, slide: Slide) -> None:
        """Add a slide to the presentation."""
        self.slides.append(slide)
    
    def to_dict(self) -> dict:
        """Convert to dictionary representation."""
        return {
            "slides": [slide.to_dict() for slide in self.slides]
        } 
