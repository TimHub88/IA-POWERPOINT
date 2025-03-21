from typing import List
from dataclasses import dataclass


@dataclass
class Slide:
    title: str
    description: str


@dataclass
class Presentation:
    slides: List[Slide]

    def add_slide(self, slide: Slide) -> None:
        self.slides.append(slide)

    @classmethod
    def create_empty(cls) -> 'Presentation':
        return cls(slides=[])