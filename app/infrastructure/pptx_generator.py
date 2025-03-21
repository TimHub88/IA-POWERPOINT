import os
from typing import Optional
import uuid
from pptx import Presentation as PPTXPresentation
from pptx.util import Inches, Pt

from ..domain.entities import Presentation, Slide
from ..domain.repository import PresentationRepository


class PPTXGenerator(PresentationRepository):
    def __init__(self, output_dir: str = "static/presentations"):
        self.output_dir = output_dir
        
        # Ensure output directory exists
        os.makedirs(self.output_dir, exist_ok=True)
    
    async def save(self, presentation: Presentation, filename: str) -> str:
        """
        Save the presentation to a PowerPoint file.
        
        Args:
            presentation: The presentation object
            filename: The filename to save as
            
        Returns:
            The path to the saved file
        """
        # Create a new PowerPoint presentation
        pptx = PPTXPresentation()
        
        # Remove the default slide
        if len(pptx.slides) > 0:
            r_id = pptx.slides._sldIdLst[0].rId
            pptx.part.drop_rel(r_id)
            pptx.slides._sldIdLst.remove(pptx.slides._sldIdLst[0])
        
        # Add slides
        for slide in presentation.slides:
            self._add_slide(pptx, slide)
        
        # Save the presentation
        file_path = os.path.join(self.output_dir, filename)
        pptx.save(file_path)
        
        # Return the relative path to be used in URLs
        return os.path.join("presentations", filename)
    
    def _add_slide(self, pptx: PPTXPresentation, slide: Slide) -> None:
        """
        Add a slide to the PowerPoint presentation.
        
        Args:
            pptx: The PowerPoint presentation object
            slide: The slide to add
        """
        # Add a slide with a title and content layout
        layout = pptx.slide_layouts[1]  # Title and Content layout
        pptx_slide = pptx.slides.add_slide(layout)
        
        # Set the title
        title = pptx_slide.shapes.title
        title.text = slide.title
        
        # Set the content
        content = pptx_slide.placeholders[1]
        content.text = slide.description
        
        # Format text (optional)
        for paragraph in content.text_frame.paragraphs:
            paragraph.font.size = Pt(18)