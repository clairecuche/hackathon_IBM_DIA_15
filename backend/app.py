"""
FastAPI application qui expose l'endpoint de prédiction.
Utilise l'orchestrateur pour gérer le flux complet de traitement.
"""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Optional, Any
import os

from . import orchestrator

app = FastAPI(
    title="LLM Energy & CO2 Predictor",
    description="API pour prédire la consommation énergétique et les émissions CO2 des requêtes LLM",
    version="1.0.0"
)


class PredictRequest(BaseModel):
    prompt: str
    model_name: str = "llama3.2"
    country: Optional[str] = None
    temperature: float = 0.7
    
    class Config:
        schema_extra = {
            "example": {
                "prompt": "Explique-moi ce qu'est l'intelligence artificielle en 3 phrases.",
                "model_name": "llama3.2",
                "country": "France",
                "temperature": 0.7
            }
        }


class PredictionResponse(BaseModel):
    llama_response: str
    energy_consumption_kwh: float
    co2_emissions_kg: Optional[float] = None
    processing_time: Dict[str, float]
    llama_metrics: Dict[str, Any]
    transformed_metrics: Optional[Dict[str, Any]] = None
    raw_ibm_response: Optional[Dict[str, Any]] = None
    equivalents: Optional[Dict[str, Any]] = None



@app.post("/predict", response_model=PredictionResponse)
async def predict(req: PredictRequest) -> PredictionResponse:
    """
    Point d'entrée principal qui reçoit un prompt et retourne la prédiction d'énergie et CO2.
    
    Args:
        req: PredictRequest contenant:
            - prompt: Le texte à envoyer au modèle
            - model_name: Nom du modèle Ollama (llama3.2, llama3.1, codellama:7b, etc.)
            - country: Code pays optionnel pour calcul CO2 (ex: "France", "USA", "Germany")
            - temperature: Créativité du modèle (0-1, default: 0.7)
    
    Returns:
        PredictionResponse avec:
            - llama_response: La réponse générée par Llama
            - energy_consumption_kwh: Consommation énergétique prédite en kWh
            - co2_emissions_kg: Émissions CO2 en kgCO2e (si pays fourni)
            - processing_time: Détail des temps d'exécution de chaque étape
            - llama_metrics: Métriques brutes de Llama
            - transformed_metrics: Métriques transformées pour IBM
            - raw_ibm_response: Réponse brute d'IBM (debug)
    """
    try:
        # Appel de l'orchestrateur qui gère tout le flux
        result = orchestrator.process_prompt(
            prompt=req.prompt,
            model_name=req.model_name,
            country=req.country,
            temperature=req.temperature
        )
        
        # Construction de la réponse
        return PredictionResponse(
            llama_response=result.llama_response,
            energy_consumption_kwh=result.ibm_prediction if result.ibm_prediction is not None else 0.0,
            co2_emissions_kg=result.co2_emissions,
            processing_time=result.timings,
            llama_metrics=result.llama_metrics,
            transformed_metrics=result.transformed_metrics,
            raw_ibm_response=result.raw_responses.get("ibm"),
            equivalents=result.raw_responses.get("equivalents")
        )
        
    except RuntimeError as e:
        # Erreurs métier (Ollama non accessible, IBM API key manquante, etc.)
        error_msg = str(e)
        
        # Messages d'erreur plus explicites
        if "Ollama" in error_msg or "localhost:11434" in error_msg:
            raise HTTPException(
                status_code=503,
                detail={
                    "error": "Ollama service unavailable",
                    "message": error_msg,
                    "help": "Make sure Ollama is running on http://localhost:11434"
                }
            )
        elif "IBM_API_KEY" in error_msg:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "Configuration error",
                    "message": "IBM_API_KEY not set in environment",
                    "help": "Set the IBM_API_KEY environment variable"
                }
            )
        else:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "Processing error",
                    "message": error_msg
                }
            )
    
    except Exception as e:
        # Erreurs inattendues
        import traceback
        tb = traceback.format_exc()
        print(f"Unexpected error: {tb}")
        
        raise HTTPException(
            status_code=500,
            detail={
                "error": "Internal server error",
                "message": str(e),
                "traceback": tb
            }
        )


@app.get("/")
def root():
    """Page d'accueil avec informations sur l'API"""
    return {
        "service": "LLM Energy & CO2 Predictor",
        "description": "Prédit la consommation énergétique et les émissions CO2 des requêtes LLM",
        "version": "1.0.0",
        "endpoints": {
            "predict": {
                "method": "POST",
                "path": "/predict",
                "description": "Envoie un prompt à Llama et obtient les prédictions d'énergie et CO2",
                "example": {
                    "prompt": "Explique-moi l'IA en 3 phrases.",
                    "model_name": "llama3.2",
                    "country": "France",
                    "temperature": 0.7
                }
            },
            "health": {
                "method": "GET",
                "path": "/health",
                "description": "Vérifie l'état de santé de l'API et ses dépendances"
            },
            "models": {
                "method": "GET",
                "path": "/models",
                "description": "Liste les modèles Ollama disponibles"
            },
            "docs": {
                "path": "/docs",
                "description": "Documentation interactive OpenAPI"
            }
        }
    }


@app.get("/health")
def health_check():
    """
    Vérifie l'état de santé de l'API et ses dépendances.
    
    Returns:
        Status de l'API, Ollama et IBM
    """
    from . import llama_client
    
    status = {
        "api": "healthy",
        "ollama": "unknown",
        "ibm_api_key": "unknown"
    }
    
    # Vérification Ollama
    try:
        if llama_client.test_connection():
            status["ollama"] = "connected"
        else:
            status["ollama"] = "unreachable"
    except Exception as e:
        status["ollama"] = f"error: {str(e)}"
    
    # Vérification IBM API Key
    api_key = os.environ.get("IBM_API_KEY")
    if api_key:
        status["ibm_api_key"] = "configured"
    else:
        status["ibm_api_key"] = "missing"
    
    # Déterminer le code HTTP
    if status["ollama"] != "connected":
        return HTTPException(
            status_code=503,
            detail=status
        )
    
    if status["ibm_api_key"] != "configured":
        return HTTPException(
            status_code=500,
            detail=status
        )
    
    return status


@app.get("/models")
def list_models():
    """
    Liste les modèles Ollama disponibles localement.
    
    Returns:
        Liste des modèles avec leurs informations
    """
    from . import llama_client
    
    try:
        models = llama_client.list_models()
        return {
            "count": len(models),
            "models": models
        }
    except Exception as e:
        raise HTTPException(
            status_code=503,
            detail={
                "error": "Cannot list models",
                "message": str(e),
                "help": "Make sure Ollama is running"
            }
        )


@app.get("/favicon.ico")
def favicon():
    """Évite les 404 dans les logs du navigateur"""
    return {}


if __name__ == "__main__":
    import uvicorn
    
    print("\n" + "="*70)
    print("🚀 DÉMARRAGE DE L'API LLM ENERGY & CO2 PREDICTOR")
    print("="*70)
    print("\n📋 Vérifications préalables:")
    
    # Vérification Ollama
    from . import llama_client
    if llama_client.test_connection():
        print("  ✅ Ollama est accessible")
        models = llama_client.list_models()
        print(f"  ✅ {len(models)} modèle(s) disponible(s)")
        for model in models[:3]:  # Afficher max 3 modèles
            print(f"     - {model.get('name', 'Unknown')}")
    else:
        print("  ⚠️  Ollama n'est pas accessible")
        print("     Assure-toi qu'Ollama est lancé sur http://localhost:11434")
    
    # Vérification IBM API Key
    if os.environ.get("IBM_API_KEY"):
        print("  ✅ IBM_API_KEY est configurée")
    else:
        print("  ⚠️  IBM_API_KEY n'est pas configurée")
        print("     Définis la variable d'environnement IBM_API_KEY")
    
    print("\n" + "="*70)
    print("🌐 Serveur disponible sur:")
    print("   - http://localhost:8000")
    print("   - http://localhost:8000/docs (documentation interactive)")
    print("="*70 + "\n")
    
    uvicorn.run(
        "backend.app:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )