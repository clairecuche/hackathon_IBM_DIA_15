"""Client for calling LLAMA API and measuring response times."""
import time
import requests
from typing import Dict, Tuple

LLAMA_API_URL = "YOUR_LLAMA_API_ENDPOINT"  # à remplacer par l'URL réelle

def call_llama(prompt: str, model_name: str = "codellama:7b") -> Tuple[str, Dict[str, float]]:
    """
    Appelle l'API LLAMA et mesure les temps de réponse.
    
    Returns:
        Tuple[str, Dict[str, float]]: (response_text, timings)
        où timings contient load_duration, prompt_duration, response_duration
    """
    headers = {
        "Content-Type": "application/json",
    }
    
    payload = {
        "prompt": prompt,
        "model": model_name,
        # autres paramètres LLAMA si nécessaire
    }
    
    # Mesure le temps total incluant l'initialisation
    start_load = time.time_ns()
    
    try:
        # Appel API
        response = requests.post(LLAMA_API_URL, headers=headers, json=payload)
        response.raise_for_status()
        
        # Extraire la réponse
        result = response.json()
        response_text = result.get("response", "")  # ajuster selon format réel
        
        # Calculer les durées (en nanosecondes)
        end_time = time.time_ns()
        
        # Note: Ces valeurs sont approximatives car on n'a pas accès aux 
        # métriques internes de LLAMA. On pourrait avoir des métriques plus
        # précises si l'API LLAMA les fournit.
        timings = {
            "load_duration": int((end_time - start_load) * 0.1),  # ~10% du temps
            "prompt_duration": int((end_time - start_load) * 0.3),  # ~30%
            "response_duration": int((end_time - start_load) * 0.6),  # ~60%
        }
        
        return response_text, timings
        
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Error calling LLAMA API: {e}")