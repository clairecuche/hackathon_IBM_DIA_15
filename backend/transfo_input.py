from transformers import AutoTokenizer

# Encodage des modèles
MODEL_ENCODING = {
    "codellama": 0,
    "codellama:70b": 1,
    "codellama:7b": 2,
    "gemma:2b": 3,
    "gemma:7b": 4,
    "llama3": 5,
    "llama3:70b": 6
}

def encode_model(model_name: str) -> int:
    """Encode le nom du modèle en entier."""
    return MODEL_ENCODING.get(model_name, -1)

def calculate_metrics_from_texts(prompt: str, response: str,
                                 load_duration: float,
                                 prompt_duration: float,
                                 response_duration: float,
                                 model_name: str) -> dict:
    """
    Calcule tous les indicateurs à partir du prompt et de la réponse.
    
    Durées en nanosecondes (ns).
    """
    # Validation des durées et utilisation d'une valeur minimale de 1ns si nécessaire
    load_duration = max(1, load_duration)
    prompt_duration = max(1, prompt_duration)
    response_duration = max(1, response_duration)

    # Charger le tokenizer correspondant au modèle
    #tokenizer = AutoTokenizer.from_pretrained(model_name.split(":")[0])
    tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")

    # Calcul des longueurs en tokens
    prompt_token_length = len(tokenizer.encode(prompt))
    response_token_length = len(tokenizer.encode(response))
    total_token_length = prompt_token_length + response_token_length

    # Calcul des vitesses en tokens/sec
    prompt_speed_tps = prompt_token_length / (prompt_duration / 1e9)
    response_speed_tps = response_token_length / (response_duration / 1e9)

    # Calcul de la durée totale
    total_inference_duration = load_duration + prompt_duration + response_duration

    metrics = {
        "prompt_speed_tps": prompt_speed_tps,
        "response_speed_tps": response_speed_tps,
        "load_duration": load_duration,
        "prompt_duration": prompt_duration,
        "response_duration": response_duration,
        "total_duration": total_inference_duration,
        "total_inference_duration": total_inference_duration,
        "prompt_token_length": prompt_token_length,
        "response_token_length": response_token_length,
        "total_token_length": total_token_length,
        "model_name_encoded": encode_model(model_name)
    }

    return metrics

"""
#Exemple d'utilisation 
if __name__ == "__main__":
    prompt = "Bonjour, comment ça va ?"
    response = "Je vais bien, merci ! Et toi ?"
    load_duration = 500000000        # ns
    prompt_duration = 1000000000    # ns
    response_duration = 2000000000  # ns
    model_name = "codellama:7b"

    metrics = calculate_metrics_from_texts(prompt, response,
                                           load_duration,
                                           prompt_duration,
                                           response_duration,
                                           model_name)
    print("\n=== MÉTRIQUES CALCULÉES ===")
    for key, value in metrics.items():
        print(f"{key}: {value}")
"""