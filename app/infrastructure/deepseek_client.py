import json
import os
from typing import Dict, List, Optional, Any
import httpx
from dotenv import load_dotenv

from ..domain.entities import Presentation, Slide
from ..domain.repository import AIContentGenerator

load_dotenv()


class DeepseekClient(AIContentGenerator):
    def __init__(self):
        self.api_key = os.getenv("DEEPSEEK_API_KEY")
        self.api_url = os.getenv("DEEPSEEK_API_URL")
        
        if not self.api_key or not self.api_url:
            raise ValueError("Missing Deepseek API credentials. Please set DEEPSEEK_API_KEY and DEEPSEEK_API_URL environment variables.")

    async def generate_presentation(self, prompt: str) -> Optional[Presentation]:
        """
        Generate a presentation using the Deepseek API.
        
        Args:
            prompt: The user prompt
            
        Returns:
            A Presentation object or None if generation failed
        """
        try:
            system_message = """
            You are a professional presentation designer. Create a structured PowerPoint presentation based on the user's prompt.
            Your output must be a valid JSON array of slides. Each slide must have:
            1. "title": a concise title for the slide
            2. "description": detailed content for the slide
            
            Format your response ONLY as a valid JSON array of objects. Do not include any explanations or additional text.
            Example format:
            [
                {"title": "Introduction", "description": "This is the introduction slide."},
                {"title": "Key Points", "description": "These are the key points."}
            ]
            """
            
            messages = [
                {"role": "system", "content": system_message},
                {"role": "user", "content": prompt}
            ]
            
            async with httpx.AsyncClient(timeout=120.0) as client:
                headers = {
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {self.api_key}"
                }
                payload = {
                    "model": "deepseek-chat",
                    "messages": messages,
                    "temperature": 0.7,
                    "max_tokens": 2000
                }
                
                response = await client.post(
                    self.api_url,
                    headers=headers,
                    json=payload
                )
                
                response.raise_for_status()
                response_data = response.json()
                
                # Extract the content from the response
                content = response_data["choices"][0]["message"]["content"]
                
                # Parse the JSON content to get slides
                slides_data = json.loads(content)
                
                # Create a Presentation object
                presentation = Presentation.create_empty()
                
                for slide_data in slides_data:
                    slide = Slide(
                        title=slide_data["title"],
                        description=slide_data["description"]
                    )
                    presentation.add_slide(slide)
                
                return presentation
                
        except Exception as e:
            print(f"Error generating presentation: {str(e)}")
            return None