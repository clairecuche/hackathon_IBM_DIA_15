"""
FastAPI application qui expose l'endpoint de prédiction.
Utilise l'orchestrateur pour gérer le flux complet de traitement.
"""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Optional, Union, List, Any
import os

from . import orchestrator

app = FastAPI(title="LLM Energy & CO2 Predictor")

class PredictRequest(BaseModel):
    prompt: str
    model_name: str = "codellama:7b"
    country: Optional[str] = None

class PredictionResponse(BaseModel):
    llama_response: str
    energy_consumption_kwh: float
    co2_emissions: Optional[float] = None  # kgCO2e
    processing_time: Dict[str, float]
    raw_response: Optional[Dict[str, Any]] = None  # Pour stocker la réponse brute d'IBM

@app.post("/predict", response_model=PredictionResponse)
async def predict(req: PredictRequest) -> PredictionResponse:
    """
    Point d'entrée principal qui reçoit un prompt et retourne la prédiction d'énergie et CO2.
    
    Args:
        req: PredictRequest contenant le prompt, nom du modèle et pays optionnel
    
    Returns:
        PredictionResponse avec la réponse LLAMA, consommation énergétique et CO2 si pays fourni
    """
    try:
        # Appel de l'orchestrateur qui gère tout le flux
        result = orchestrator.process_prompt(
            prompt=req.prompt,
            model_name=req.model_name,
            country=req.country
        )
        
        # Construction de la réponse
        return PredictionResponse(
            llama_response=result.llama_response,
            energy_consumption_kwh=result.ibm_prediction 
                if result.ibm_prediction is not None else 0.0,
            co2_emissions=result.co2_emissions,
            processing_time=result.timings,
            raw_response=result.raw_responses.get("ibm")
        )
        
    except Exception as e:
        # Log l'erreur et renvoie une réponse 500
        print(f"Error processing request: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error processing request: {str(e)}"
        )

@app.get("/")
def root():
    """Simple root to make visiting / in a browser useful instead of 404."""
    return {
        "message": "LLM Energy & CO2 Predictor",
        "endpoints": {
            "predict": {
                "method": "POST",
                "path": "/predict",
                "description": "Send JSON {\"prompt\": \"your text\", \"model_name\": \"codellama:7b\", \"country\": \"France\"}",
            },
            "docs": {"path": "/docs", "description": "Interactive OpenAPI docs"},
        },
    }

@app.get("/favicon.ico")
def favicon():
    """Return no content to avoid 404 in browser logs"""
    return {}
    # ensure API key available
    # If the client provided metric fields directly, use them and skip the
    # IBM call. Otherwise, if a prompt is present, call the IBM deployment to
    # obtain metrics. If neither metrics nor prompt are provided, return an
    # error.

    raw = None

    def build_ordered_values():
        # If client provided raw input_values, try to reorder them to the
        # FIXED_INPUT_FIELDS order.
        if getattr(req, "input_values", None):
            provided_fields = getattr(req, "input_fields", None) or []
            # take only the first row if multiple provided, and map by index
            provided_row = req.input_values[0] if req.input_values else []
            # Build a row following FIXED_INPUT_FIELDS by matching indexes
            ordered_row = []
            for f in FIXED_INPUT_FIELDS:
                if f in provided_fields:
                    idx = provided_fields.index(f)
                    # safe-get value from provided_row
                    try:
                        ordered_row.append(provided_row[idx])
                    except Exception:
                        ordered_row.append(0)
                else:
                    # field not present in provided_fields -> fill from
                    # explicit metric attributes or sensible defaults
                    if f == "COLUMN1":
                        ordered_row.append(1)
                    elif f == "model_name_encoded":
                        # prefer explicit numeric encoded value, else map name
                        if getattr(req, "model_name_encoded", None) is not None:
                            ordered_row.append(req.model_name_encoded)
                        elif getattr(req, "model_name", None):
                            code = MODEL_NAME_MAP.get(req.model_name.strip().lower())
                            ordered_row.append(code if code is not None else 0)
                        else:
                            ordered_row.append(0)
                    else:
                        val = getattr(req, f, None)
                        ordered_row.append(val if val is not None else 0)
            return [ordered_row]

        # No input_values provided: build from individual metric fields
        row = []
        for f in FIXED_INPUT_FIELDS:
            if f == "COLUMN1":
                row.append(1)
                continue
            if f == "model_name_encoded":
                if getattr(req, "model_name_encoded", None) is not None:
                    row.append(req.model_name_encoded)
                elif getattr(req, "model_name", None):
                    code = MODEL_NAME_MAP.get(req.model_name.strip().lower())
                    row.append(code if code is not None else 0)
                else:
                    row.append(0)
                continue
            # other numeric metric fields
            row.append(getattr(req, f, 0) or 0)

        return [row]

    # Always call IBM with the fixed fields/ordered values
    api_key = os.environ.get("IBM_API_KEY")
    if not api_key:
        raise HTTPException(status_code=500, detail="IBM_API_KEY not set in environment")
    try:
        values = build_ordered_values()
        raw = ibm_client.score_prompt(
            prompt=None,
            api_key=api_key,
            fields=FIXED_INPUT_FIELDS,
            values=values,
        )
    except Exception as e:
        tb = traceback.format_exc()
        raise HTTPException(status_code=502, detail=f"Error calling IBM ML: {e}\n{tb}")

    metrics = ibm_client.extract_metrics(raw, prompt=req.prompt)
    # If the request included a human-readable model_name or an explicit
    # model_name_encoded prefer those values to override the scored output.
    if req.model_name:
        code = MODEL_NAME_MAP.get(req.model_name.strip().lower())
        if code is not None:
            metrics["model_name_encoded"] = code
    if getattr(req, "model_name_encoded", None) is not None:
        metrics["model_name_encoded"] = getattr(req, "model_name_encoded")


    prediction_energy = 0.0

    try:
        if (raw and raw.get("predictions") and len(raw["predictions"]) > 0
            and raw["predictions"][0].get("values")
            and len(raw["predictions"][0]["values"]) > 0
            and len(raw["predictions"][0]["values"][0]) > 0):
            prediction_energy= raw["predictions"][0]["values"][0][0]
        
    except Exception:
        prediction_energy= None

    print(prediction_energy)

    # Determine energy in kgCo2e: compute from provided country, else None
    computed_co2e_kg = None
    computed_co2e_kg = energy.compute_co2e_kg(prediction_energy, req.country)

    resp = {
        "prediction_energy": prediction_energy,
        "computed_co2e_kg" : computed_co2e_kg,

        
    }

    # extract total consumption reported by the model (seconds) and attach
    try:
        consumption = predictor.extract_total_consumption(metrics, raw_response=raw)
        resp["consumption"] = consumption
    except Exception:
        resp["consumption"] = {"total_consumption": None, "units": "seconds", "source_field": None}

    return resp


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.app:app", host="0.0.0.0", port=8000, reload=True)