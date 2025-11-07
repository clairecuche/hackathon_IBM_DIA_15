"""
Orchestrateur central qui gère le flux complet :
1. Réception du prompt
2. Appel LLAMA via llama_client
3. Transformation des données via transfo_input
4. Prédiction énergie via IBM
5. Calcul CO2 si pays fourni
"""
from typing import Dict, Any, Optional
import time
from datetime import datetime
import json
import os

from . import llama_client
from . import transfo_input
from . import ibm_client
from . import energy


class TimingLogger:
    """Structure pour stocker les logs de timing de chaque étape"""
    def __init__(self):
        self.start_time = time.time_ns()
        self.steps = {}
    
    def log_step(self, step_name: str):
        self.steps[step_name] = time.time_ns() - self.start_time
    
    def get_timings(self) -> Dict[str, float]:
        return {k: v for k, v in self.steps.items()}  # convertit en secondes


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
    model_name: str = "llama3.2",
    country: Optional[str] = None,
    log_file: Optional[str] = "logs/processing.jsonl",
    temperature: float = 0.7
) -> ProcessingResult:
    """
    Fonction principale qui orchestre tout le flux de traitement.
    
    Args:
        prompt: Le texte à envoyer à LLAMA
        model_name: Le modèle à utiliser (llama3.2, llama3.1, codellama:7b, etc.)
        country: Code pays optionnel pour calcul CO2
        log_file: Chemin pour sauvegarder les logs (default: logs/processing.jsonl)
        temperature: Créativité du modèle (0-1)
    
    Returns:
        ProcessingResult avec tous les résultats intermédiaires et finaux
    """
    timing = TimingLogger()
    result = ProcessingResult()
    
    try:
        # 1. Appel à LLAMA via Ollama
        print(f"📡 Appel à Llama ({model_name})...")
        timing.log_step("llama_start")
        
        result.llama_response, result.llama_metrics = llama_client.call_llama(
            prompt=prompt,
            model_name=model_name,
            temperature=temperature
        )
        
        timing.log_step("llama_end")
        print(f"✅ Réponse Llama reçue ({len(result.llama_response)} caractères)")
        
        # 2. Transformation des métriques
        print("🔄 Transformation des métriques...")
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
        print("✅ Métriques transformées")
        
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
        print("🔮 Appel à IBM Watson pour prédiction d'énergie...")
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
            print(f"✅ Prédiction énergie: {result.ibm_prediction:.6f} kWh")
        else:
            print("⚠️  Aucune prédiction d'énergie reçue d'IBM")
            
        timing.log_step("ibm_call_end")
        result.ibm_prediction = result.ibm_prediction/1000 if result.ibm_prediction is not None else None
        # 5. Calcul CO2 si pays fourni
        if country:
            print(f"🌍 Calcul des émissions CO2 pour {country}...")
            timing.log_step("co2_calc_start")
            
            result.co2_emissions = energy.compute_co2e_kg(
                energy_consumption_llm_total_kwh=result.ibm_prediction if result.ibm_prediction is not None else 0.0,
                country=country
            )
            
            timing.log_step("co2_calc_end")
            print(f"✅ Émissions CO2: {result.co2_emissions:.6f} kgCO2e")

        # Use total_duration (in seconds) for equivalents (with fallback to timings)
        tm = result.transformed_metrics or {}
        duration_seconds = None
        if tm.get("total_duration") is not None:
            try:
                duration_seconds = float(tm["total_duration"])
            except Exception:
                duration_seconds = None

        # fallback: approximate from recorded timings if available
        if duration_seconds is None and result.timings:
            try:
                duration_seconds = sum(float(v) for v in result.timings.values() if v is not None)
            except Exception:
                duration_seconds = None

        # compute equivalents if possible, otherwise store empty dict so API returns {} not null
        equivalents = {}
        if result.co2_emissions is not None and duration_seconds and duration_seconds > 0:
            acres = energy.forest_area_acres(result.co2_emissions, duration_seconds)
            searches = energy.co2e_to_google_searches(result.co2_emissions)
            equivalents = {
                "forest_area_acres": acres,
                "google_searches": searches,
                "duration_seconds_used": duration_seconds,
            }

        # always set the key (even if empty) so callers don't get null
        result.raw_responses["equivalents"] = equivalents

        
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
            with open(log_file, "a", encoding="utf-8") as f:
                f.write(json.dumps(log_entry, ensure_ascii=False) + "\n")
        
        print("✅ Traitement terminé avec succès")
        return result
        
    except Exception as e:
        # Log l'erreur
        print(f"❌ Erreur lors du traitement: {str(e)}")
        
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
            with open(log_file, "a", encoding="utf-8") as f:
                f.write(json.dumps(error_entry, ensure_ascii=False) + "\n")
        
        # Propage l'erreur pour gestion par l'appelant
        raise


# Test si exécuté directement
if __name__ == "__main__":
    print("\n" + "="*70)
    print("🧪 TEST DE L'ORCHESTRATEUR")
    print("="*70 + "\n")
    
    # Test avec un prompt simple
    test_prompt = "Explique-moi ce qu'est le machine learning en 2 phrases."
    
    try:
        result = process_prompt(
            prompt=test_prompt,
            model_name="llama3.2",
            country="France",
            temperature=0.7
        )
        
        print("\n" + "="*70)
        print("📊 RÉSULTATS FINAUX")
        print("="*70)
        print(f"\n💬 Prompt: {test_prompt}")
        print(f"\n🤖 Réponse Llama:\n{result.llama_response}")
        print(f"\n⚡ Consommation énergétique: {result.ibm_prediction:.6f} kWh")
        print(f"🌍 Émissions CO2: {result.co2_emissions:.6f} kgCO2e")
        print(f"\n⏱️  Temps de traitement:")
        for step, duration in result.timings.items():
            print(f"  - {step}: {duration:.3f}s")
        
        print("\n✅ Test réussi!")
        
    except Exception as e:
        print(f"\n❌ Test échoué: {str(e)}")
        import traceback
        traceback.print_exc()