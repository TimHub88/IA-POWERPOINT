import os
import httpx
import json
from typing import Optional, List, Dict, Any
from dotenv import load_dotenv
import traceback

# Recharger les variables d'environnement
load_dotenv(override=True)

class PexelsClient:
    """Client for the Pexels API to search for relevant images based on keywords."""
    
    def __init__(self):
        # Récupérer la clé API depuis les variables d'environnement
        self.api_key = os.getenv("PEXELS_API_KEY")
        self.api_url = "https://api.pexels.com/v1/search"
        
        # Afficher des informations sur la clé API (sans la révéler entièrement)
        if not self.api_key:
            print("⚠️ Pexels API key not found in environment variables. Using fallback images.")
            self.api_key = None
        else:
            key_preview = self.api_key[:4] + "..." + self.api_key[-4:] if len(self.api_key) > 8 else "***"
            print(f"🚀 PexelsClient initialized with API key: {key_preview}")
            # Vérifier que la clé n'est pas une chaîne littérale comme "your_api_key_here"
            if "your_api_key" in self.api_key.lower():
                print("⚠️ WARNING: Your Pexels API key appears to be a placeholder. Please replace it with a real API key.")
                self.api_key = None
    
    async def search_image(self, keywords: List[str], fallback_url: str = None) -> str:
        """
        Search for an image on Pexels based on keywords.
        
        Args:
            keywords: List of keywords to search for
            fallback_url: URL to use if no image is found or API key is missing
            
        Returns:
            URL of a relevant image, or the fallback URL if none found
        """
        # Utiliser une image locale comme fallback par défaut
        local_fallback = "static/images/fallback.jpg"
        if not os.path.exists(local_fallback):
            # S'assurer que le répertoire existe
            os.makedirs("static/images", exist_ok=True)
            print(f"ℹ️ Created directory for local fallback images: static/images")
            
            # Utiliser une URL de secours si l'image locale n'existe pas
            if fallback_url:
                print(f"ℹ️ Using provided fallback URL: {fallback_url}")
            else:
                fallback_url = "https://via.placeholder.com/1600x900/e0e0e0/808080?text=No+Image+Available"
                print(f"ℹ️ Using default placeholder fallback URL")
        else:
            # Utiliser le chemin relatif pour le HTML
            fallback_url = "/static/images/fallback.jpg"
            print(f"ℹ️ Using local fallback image: {local_fallback}")
        
        # Si pas de clé API ou pas de mots-clés, retourner l'URL de secours
        if not self.api_key or not keywords:
            if not self.api_key:
                print(f"⚠️ No valid Pexels API key available")
            if not keywords:
                print(f"⚠️ No keywords provided for image search")
            return fallback_url
        
        # Nettoyer et préparer les mots-clés
        search_query = " ".join([k.strip() for k in keywords if k.strip()])
        print(f"🔍 Searching Pexels for images with keywords: '{search_query}'")
        
        try:
            # Créer un client HTTP
            print(f"🌐 Making request to Pexels API...")
            async with httpx.AsyncClient(timeout=15.0) as client:
                # Préparer les en-têtes avec la clé API
                headers = {
                    "Authorization": self.api_key,
                    "User-Agent": "PowerPoint Generator App/1.0"
                }
                print(f"🔄 Request headers prepared (Authorization: {self.api_key[:4]}...)")
                
                # Préparer les paramètres de recherche
                params = {
                    "query": search_query,
                    "per_page": 1,
                    "size": "large"
                }
                print(f"🔄 Request parameters: {params}")
                
                # Effectuer la requête
                try:
                    response = await client.get(
                        self.api_url,
                        params=params,
                        headers=headers
                    )
                    print(f"🔄 Received response with status code: {response.status_code}")
                    
                    # Afficher les en-têtes de la réponse pour débogage
                    print(f"ℹ️ Response headers: {dict(response.headers)}")
                    
                    # Vérifier si la requête a réussi
                    if response.status_code == 200:
                        # Extraire les données JSON
                        try:
                            data = response.json()
                            print(f"✅ Successfully parsed JSON response")
                            
                            # Vérifier si nous avons des résultats
                            if data.get("photos") and len(data["photos"]) > 0:
                                # Obtenir l'URL de l'image
                                image_url = data["photos"][0]["src"]["large2x"]
                                print(f"✅ Found image on Pexels: {image_url}")
                                return image_url
                            else:
                                print(f"⚠️ No images found in Pexels response for keywords: '{search_query}'")
                                return fallback_url
                        except json.JSONDecodeError as e:
                            print(f"⚠️ Failed to parse JSON from Pexels response: {str(e)}")
                            print(f"⚠️ Response content preview: {response.text[:200]}...")
                            return fallback_url
                    else:
                        print(f"⚠️ Pexels API request failed with status code: {response.status_code}")
                        print(f"⚠️ Response content preview: {response.text[:200]}...")
                        return fallback_url
                except httpx.RequestError as e:
                    print(f"⚠️ HTTP request to Pexels failed: {str(e)}")
                    return fallback_url
        
        except Exception as e:
            print(f"⚠️ Error searching Pexels: {str(e)}")
            print(f"⚠️ Traceback: {traceback.format_exc()}")
            return fallback_url 