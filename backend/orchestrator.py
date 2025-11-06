"""
Orchestrateur central qui gère le flux complet :
1. Réception du prompt
2. Appel LLAMA via llama_client
3. Transformation des données via transfo_input
4. Prédiction énergie via IBM
5. Calcul CO2 si pays fourni
"""
from typing import Dict, Any, Optional, Tuple
import time
from datetime import datetime
import json
import os

from . import llama_client
from . import transfo_input
from . import ibm_client
from . import energy

# Structure pour stocker les logs de timing de chaque étape
class TimingLogger:
    def __init__(self):
        self.start_time = time.time_ns()
        self.steps = {}
    
    def log_step(self, step_name: str):
        self.steps[step_name] = time.time_ns() - self.start_time
    
    def get_timings(self) -> Dict[str, float]:
        return {k: v/1e9 for k, v in self.steps.items()}  # convertit en secondes

class ProcessingResult:
    """Classe pour stocker et accéder facilement aux résultats de chaque étape"""
    def __init__(self):
        self.llama_response: Optional[str] = None
        self.llama_metrics: Optional[Dict[str, float]] = None
        self.transformed_metrics: Optional[Dict[str, Any]] = None
        self.ibm_prediction: Optional[float] = None  # Consommation d'énergie en kWh
        self.co2_emissions: Optional[float] = None   # Émissions CO2 en kgCO2e
        self.timings: Dict[str, float] = {}
        self.raw_responses: Dict[str, Any] = {}

def process_prompt(
    prompt: str,
    model_name: str = "codellama:7b",
    country: Optional[str] = None,
    log_file: Optional[str] = "logs/processing.jsonl"
) -> ProcessingResult:
    """
    Fonction principale qui orchestre tout le flux de traitement.
    
    Args:
        prompt: Le texte à envoyer à LLAMA
        model_name: Le modèle à utiliser (default: codellama:7b)
        country: Code pays optionnel pour calcul CO2
        log_file: Chemin pour sauvegarder les logs (default: logs/processing.jsonl)
    
    Returns:
        ProcessingResult avec tous les résultats intermédiaires et finaux
    """
    timing = TimingLogger()
    result = ProcessingResult()
    
    try:
        # 1. Appel à LLAMA
        timing.log_step("llama_start")
        result.llama_response, result.llama_metrics = llama_client.call_llama(
            prompt=prompt,
            model_name=model_name
        )
        timing.log_step("llama_end")
        
        # 2. Transformation des métriques
        timing.log_step("transform_start")
        result.transformed_metrics = transfo_input.calculate_metrics_from_texts(
            prompt=prompt,
            response=result.llama_response,
            load_duration=result.llama_metrics["load_duration"],
            prompt_duration=result.llama_metrics["prompt_duration"],
            response_duration=result.llama_metrics["response_duration"],
            model_name=model_name
        )
        timing.log_step("transform_end")
        
        # 3. Préparation payload IBM dans le bon ordre
        timing.log_step("ibm_prep_start")
        fields = [
            "COLUMN1",
            "prompt_speed_tps",
            "response_speed_tps",
            "load_duration",
            "total_inference_duration",
            "response_duration",
            "total_token_length",
            "response_token_length",
            "total_duration",
            "prompt_duration",
            "prompt_token_length",
            "model_name_encoded",
        ]
        
        values = [[
            1,  # COLUMN1 toujours 1
            result.transformed_metrics["prompt_speed_tps"],
            result.transformed_metrics["response_speed_tps"],
            result.transformed_metrics["load_duration"],
            result.transformed_metrics["total_inference_duration"],
            result.transformed_metrics["response_duration"],
            result.transformed_metrics["total_token_length"],
            result.transformed_metrics["response_token_length"],
            result.transformed_metrics["total_duration"],
            result.transformed_metrics["prompt_duration"],
            result.transformed_metrics["prompt_token_length"],
            result.transformed_metrics["model_name_encoded"]
        ]]
        timing.log_step("ibm_prep_end")
        
        # 4. Appel IBM pour prédiction énergie
        timing.log_step("ibm_call_start")
        api_key = os.environ.get("IBM_API_KEY")
        if not api_key:
            raise RuntimeError("IBM_API_KEY not set in environment")
            
        raw_ibm = ibm_client.score_prompt(
            prompt=None,
            api_key=api_key,
            fields=fields,
            values=values
        )
        result.raw_responses["ibm"] = raw_ibm
        
        # Extraction de la prédiction
        if (raw_ibm and raw_ibm.get("predictions")
            and len(raw_ibm["predictions"]) > 0
            and raw_ibm["predictions"][0].get("values")
            and len(raw_ibm["predictions"][0]["values"]) > 0):
            result.ibm_prediction = raw_ibm["predictions"][0]["values"][0][0]
        timing.log_step("ibm_call_end")
        
        # 5. Calcul CO2 si pays fourni
        if country:
            timing.log_step("co2_calc_start")
            result.co2_emissions = energy.compute_co2e_kg(
                energy_consumption_llm_total_kwh=result.ibm_prediction if result.ibm_prediction is not None else 0.0,
                country=country
            )
            timing.log_step("co2_calc_end")
        
        # Stockage des timings finaux
        result.timings = timing.get_timings()
        
        # Log des résultats si log_file spécifié
        if log_file:
            os.makedirs(os.path.dirname(log_file), exist_ok=True)
            log_entry = {
                "timestamp": datetime.utcnow().isoformat(),
                "prompt": prompt,
                "model": model_name,
                "country": country,
                "llama_metrics": result.llama_metrics,
                "transformed_metrics": result.transformed_metrics,
                "ibm_prediction": result.ibm_prediction,
                "co2_emissions": result.co2_emissions,
                "timings": result.timings
            }
            with open(log_file, "a") as f:
                f.write(json.dumps(log_entry) + "\n")
        
        return result
        
    except Exception as e:
        # Log l'erreur mais ne la propage pas
        if log_file:
            os.makedirs(os.path.dirname(log_file), exist_ok=True)
            error_entry = {
                "timestamp": datetime.utcnow().isoformat(),
                "error": str(e),
                "prompt": prompt,
                "model": model_name,
                "country": country,
                "partial_results": {
                    "llama_response": result.llama_response,
                    "llama_metrics": result.llama_metrics,
                    "transformed_metrics": result.transformed_metrics,
                    "ibm_prediction": result.ibm_prediction,
                    "timings": timing.get_timings()
                }
            }
            with open(log_file, "a") as f:
                f.write(json.dumps(error_entry) + "\n")
        
        # Propage l'erreur pour gestion par l'appelant
        raise