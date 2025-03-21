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
        
        print("🚀 DeepseekClient initialized successfully")

    async def generate_presentation(self, prompt: str, include_images: bool = True) -> Optional[Presentation]:
        """
        Generate a presentation using the Deepseek API.
        
        Args:
            prompt: The user prompt
            include_images: Whether to include images in the presentation
            
        Returns:
            A Presentation object or None if generation failed
        """
        try:
            print(f"🔍 Starting presentation generation for prompt: '{prompt[:50]}...'")
            
            # Utiliser le paramètre include_images passé à la fonction
            print(f"🔄 Image generation mode: {'enabled' if include_images else 'disabled'}")
            
            # Message système pour la génération avec ou sans images
            if include_images:
                system_message = """
                You are a professional presentation designer. Create a structured PowerPoint presentation based on the user's prompt.
                Your output must be a valid JSON array of slides. Each slide must have:
                1. "title": a concise title for the slide
                2. "description": detailed content for the slide
                3. "keywords": an array of 3-5 specific keywords that best describe the visual content needed for this slide
                4. "image": leave this field blank - it will be filled in later with an image URL

                For the keywords:
                - Choose specific and descriptive terms that clearly represent what should be shown in the image
                - Include concrete nouns and adjectives that can be visually represented
                - Avoid abstract concepts that cannot be directly visualized
                - Focus on the key visual elements that would enhance the slide content
                - Be precise rather than general (e.g. "office workers collaborating" instead of just "business")

                Format your response ONLY as a valid JSON array of objects. Do not include any explanations or additional text.
                Example format:
                [
                    {
                        "title": "Introduction to Renewable Energy",
                        "description": "Renewable energy sources include solar, wind, hydroelectric, and geothermal power. These sustainable alternatives are essential for reducing carbon emissions.",
                        "keywords": ["solar panels", "wind turbines", "renewable energy technology", "green power", "sustainable energy"]
                    },
                    {
                        "title": "Benefits of Solar Power",
                        "description": "Solar energy provides clean, renewable power with minimal environmental impact. Modern photovoltaic cells are increasingly efficient and affordable.",
                        "keywords": ["solar panel installation", "rooftop solar array", "sunlight energy conversion", "modern solar technology", "photovoltaic cells"]
                    }
                ]
                """
            else:
                system_message = """
                You are a professional presentation designer. Create a structured PowerPoint presentation based on the user's prompt.
                Your output must be a valid JSON array of slides. Each slide must have:
                1. "title": a concise title for the slide
                2. "description": detailed content for the slide

                Focus solely on creating high-quality textual content. Do not include keywords or image-related information.

                Format your response ONLY as a valid JSON array of objects. Do not include any explanations or additional text.
                Example format:
                [
                    {
                        "title": "Introduction to Renewable Energy",
                        "description": "Renewable energy sources include solar, wind, hydroelectric, and geothermal power. These sustainable alternatives are essential for reducing carbon emissions."
                    },
                    {
                        "title": "Benefits of Solar Power",
                        "description": "Solar energy provides clean, renewable power with minimal environmental impact. Modern photovoltaic cells are increasingly efficient and affordable."
                    }
                ]
                """
            
            messages = [
                {"role": "system", "content": system_message},
                {"role": "user", "content": prompt}
            ]
            
            print("🔄 Preparing API request to Deepseek")
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
                
                print("🛠️ Sending request to Deepseek API")
                response = await client.post(
                    self.api_url,
                    headers=headers,
                    json=payload
                )
                
                response.raise_for_status()
                print("✅ Received response from Deepseek API")
                response_data = response.json()
                
                # Extract the content from the response
                content = response_data["choices"][0]["message"]["content"]
                
                # Parse the JSON content to get slides
                print("🔄 Parsing JSON response from Deepseek")
                try:
                    slides_data = json.loads(content)
                    print(f"✅ Successfully parsed JSON with {len(slides_data)} slides")
                except json.JSONDecodeError as e:
                    print(f"⚠️ JSON parsing error: {str(e)}")
                    print(f"⚠️ Raw content received: {content[:200]}...")
                    raise
                
                # Create a Presentation object
                presentation = Presentation.create_empty()
                
                print("🛠️ Creating slides objects from API response")
                for i, slide_data in enumerate(slides_data):
                    # Log each slide being created with its keywords
                    title = slide_data["title"]
                    
                    # Gérer les keywords en fonction du mode (avec ou sans images)
                    keywords = slide_data.get("keywords", [])
                    if include_images:
                        keywords_str = ", ".join(keywords) if keywords else "No keywords provided"
                        print(f"🔷 Slide {i+1}: '{title}' with keywords: {keywords_str}")
                    else:
                        print(f"🔷 Slide {i+1}: '{title}' (no images mode)")
                    
                    slide = Slide(
                        title=slide_data["title"],
                        description=slide_data["description"],
                        image=slide_data.get("image", ""),  # This will likely be empty and filled later
                        keywords=keywords  # Get keywords for image search
                    )
                    presentation.add_slide(slide)
                
                if include_images:
                    print(f"✅ Presentation generation complete - {len(presentation.slides)} slides created with image support")
                else:
                    print(f"✅ Presentation generation complete - {len(presentation.slides)} slides created without images")
                return presentation
                
        except Exception as e:
            print(f"⚠️ Error generating presentation: {str(e)}")
            import traceback
            print(f"⚠️ Traceback: {traceback.format_exc()}")
            return None 
