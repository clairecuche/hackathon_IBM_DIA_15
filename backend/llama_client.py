"""
Client pour appeler l'API Ollama et récupérer les métriques Llama.
"""
import requests
from typing import Tuple, Dict


def call_llama(
    prompt: str, 
    model_name: str = "llama3.2", 
    temperature: float = 0.7,
    base_url: str = "http://localhost:11434"
) -> Tuple[str, Dict[str, float]]:
    """
    Appelle l'API Ollama et retourne la réponse + métriques.
    
    Args:
        prompt: Le texte à envoyer au modèle
        model_name: Nom du modèle Ollama (llama3.2, llama3.1, codellama:7b, etc.)
        temperature: Créativité du modèle (0-1)
        base_url: URL de l'API Ollama
    
    Returns:
        Tuple (response_str, metrics_dict) où metrics_dict contient:
            - load_duration (float): Temps de chargement du modèle en secondes
            - prompt_duration (float): Temps de traitement du prompt en secondes
            - response_duration (float): Temps de génération de la réponse en secondes
            - total_duration (float): Durée totale en secondes
            - model_name (str): Nom du modèle utilisé
    
    Raises:
        RuntimeError: Si l'appel à Ollama échoue
    """
    generate_url = f"{base_url}/api/generate"
    
    payload = {
        "model": model_name,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": temperature
        }
    }
    
    try:
        response = requests.post(generate_url, json=payload, timeout=300)
        
        if response.status_code != 200:
            raise RuntimeError(
                f"Ollama API error: {response.status_code} - {response.text}"
            )
        
        data = response.json()
        
        # Conversion nanosecondes → secondes
        ns_to_s = 1e-9
        
        # Construction du dictionnaire de métriques
        metrics_dict = {
            "load_duration": data.get('load_duration', 0) * ns_to_s,
            "prompt_duration": data.get('prompt_eval_duration', 0) * ns_to_s,
            "response_duration": data.get('eval_duration', 0) * ns_to_s,
            "total_duration": data.get('total_duration', 0) * ns_to_s,
            "model_name": data.get('model', model_name),
        }
        
        response_text = data.get('response', '')
        
        if not response_text:
            raise RuntimeError("Ollama returned empty response")
        
        return response_text, metrics_dict
        
    except requests.exceptions.Timeout:
        raise RuntimeError("Timeout: Ollama took too long to respond (>300s)")
    except requests.exceptions.ConnectionError:
        raise RuntimeError(
            "Connection error: Cannot reach Ollama at {base_url}. "
            "Make sure Ollama is running (it should start automatically on Windows)"
        )
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Request error when calling Ollama: {str(e)}")
    except KeyError as e:
        raise RuntimeError(f"Unexpected response format from Ollama: missing key {e}")
    except Exception as e:
        raise RuntimeError(f"Unexpected error calling Ollama: {str(e)}")


def test_connection(base_url: str = "http://localhost:11434") -> bool:
    """
    Teste si Ollama est accessible.
    
    Returns:
        True si Ollama répond, False sinon
    """
    try:
        response = requests.get(base_url, timeout=5)
        return response.status_code == 200
    except:
        return False


def list_models(base_url: str = "http://localhost:11434") -> list:
    """
    Liste les modèles Ollama disponibles.
    
    Returns:
        Liste des modèles disponibles
    """
    try:
        response = requests.get(f"{base_url}/api/tags", timeout=5)
        if response.status_code == 200:
            return response.json().get('models', [])
        return []
    except:
        return []


# Test si exécuté directement
if __name__ == "__main__":
    print("🔍 Test de connexion à Ollama...")
    
    if not test_connection():
        print("❌ Ollama n'est pas accessible sur http://localhost:11434")
        print("💡 Assure-toi qu'Ollama est lancé")
        exit(1)
    
    print("✅ Connexion réussie!\n")
    
    print("📦 Modèles disponibles:")
    models = list_models()
    for model in models:
        print(f"  - {model.get('name', 'Unknown')}")
    
    print("\n🚀 Test d'appel à Llama...")
    try:
        response, metrics = call_llama(
            prompt="Dis bonjour en une phrase.",
            model_name="llama3.2"
        )
        
        print(f"\n💬 Réponse: {response}")
        print(f"\n⏱️  Métriques:")
        for key, value in metrics.items():
            if isinstance(value, float):
                print(f"  - {key}: {value:.3f}s")
            else:
                print(f"  - {key}: {value}")
        
        print("\n✅ Test réussi!")
        
    except RuntimeError as e:
        print(f"\n❌ Erreur: {e}")