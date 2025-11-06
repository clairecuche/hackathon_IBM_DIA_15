import requests
import json
from dataclasses import dataclass


@dataclass
class LlamaMetrics:
    """Classe pour stocker toutes les métriques"""
    prompt: str
    response: str
    load_duration: float
    prompt_duration: float
    response_duration: float
    model_name: str
    total_duration: float = 0.0
    
    def afficher(self):
        """Affiche les métriques de manière claire"""
        print("\n" + "="*70)
        print("📊 RÉSULTATS LLAMA 3.2")
        print("="*70)
        print(f"\n💬 Prompt:\n{self.prompt}\n")
        print(f"🤖 Réponse:\n{self.response}\n")
        print("⏱️  MÉTRIQUES DE PERFORMANCE:")
        print(f"  └─ Chargement du modèle    : {self.load_duration:.3f}s")
        print(f"  └─ Traitement du prompt    : {self.prompt_duration:.3f}s")
        print(f"  └─ Génération de la réponse: {self.response_duration:.3f}s")
        print(f"  └─ DURÉE TOTALE            : {self.total_duration:.3f}s")
        print(f"\n🏷️  Modèle utilisé: {self.model_name}")
        print("="*70 + "\n")


class OllamaClient:
    """Client simplifié pour Ollama"""
    
    def __init__(self, base_url="http://localhost:11434"):
        self.base_url = base_url
        self.generate_url = f"{base_url}/api/generate"
    
    def test_connexion(self):
        """Teste si Ollama répond"""
        try:
            response = requests.get(self.base_url, timeout=5)
            return response.status_code == 200
        except:
            return False
    
    def generate(self, prompt, model="llama3.2", temperature=0.7):
        """Envoie un prompt et récupère toutes les métriques"""
        
        payload = {
            "model": model,
            "prompt": prompt,
            "stream": False,
            "options": {"temperature": temperature}
        }
        
        try:
            print(f"⏳ Envoi du prompt au modèle {model}...")
            response = requests.post(self.generate_url, json=payload, timeout=300)
            
            if response.status_code == 200:
                data = response.json()
                
                # Conversion nanosecondes → secondes
                ns_to_s = 1e-9
                
                return LlamaMetrics(
                    prompt=prompt,
                    response=data.get('response', ''),
                    load_duration=data.get('load_duration', 0) * ns_to_s,
                    prompt_duration=data.get('prompt_eval_duration', 0) * ns_to_s,
                    response_duration=data.get('eval_duration', 0) * ns_to_s,
                    model_name=data.get('model', model),
                    total_duration=data.get('total_duration', 0) * ns_to_s
                )
            else:
                print(f"❌ Erreur API: {response.status_code}")
                print(response.text)
                return None
                
        except requests.exceptions.Timeout:
            print("❌ Timeout: le modèle met trop de temps à répondre")
            return None
        except Exception as e:
            print(f"❌ Erreur: {e}")
            return None


# 🎯 TEST PRINCIPAL
if __name__ == "__main__":
    print("\n" + "🚀 TEST OLLAMA LLAMA 3.2 ".center(70, "="))
    
    # Étape 1: Vérifier la connexion
    print("\n1️⃣  Vérification de la connexion à Ollama...")
    client = OllamaClient()
    
    if not client.test_connexion():
        print("❌ ERREUR: Ollama n'est pas accessible!")
        print("\n💡 Solutions:")
        print("   - Vérifie que le service Ollama est lancé")
        print("   - Redémarre ton PC (Ollama se lance au démarrage)")
        print("   - Vérifie dans le gestionnaire des tâches si 'ollama' est actif")
        exit(1)
    
    print("✅ Connexion réussie!\n")
    
    # Étape 2: Test simple
    print("2️⃣  Test avec un prompt simple...")
    prompt_test = "Dis bonjour en une phrase."
    
    metrics = client.generate(prompt_test, model="llama3.2")
    
    if metrics:
        metrics.afficher()
        
        # Exemple d'accès aux valeurs individuelles
        print("\n📌 ACCÈS AUX DONNÉES INDIVIDUELLES:")
        print(f"   metrics.prompt             = '{metrics.prompt}'")
        print(f"   metrics.response           = '{metrics.response[:50]}...'")
        print(f"   metrics.load_duration      = {metrics.load_duration:.3f} secondes")
        print(f"   metrics.prompt_duration    = {metrics.prompt_duration:.3f} secondes")
        print(f"   metrics.response_duration  = {metrics.response_duration:.3f} secondes")
        print(f"   metrics.model_name         = '{metrics.model_name}'")
        print(f"   metrics.total_duration     = {metrics.total_duration:.3f} secondes")
        
        print("\n✅ TEST RÉUSSI! Tu peux maintenant utiliser le code complet.")
    else:
        print("❌ Échec du test")
    
    print("\n" + "="*70 + "\n")


# 💡 EXEMPLES D'UTILISATION SUPPLÉMENTAIRES

def exemple_questions_multiples():
    """Teste plusieurs prompts à la suite"""
    client = OllamaClient()
    
    questions = [
        "Qu'est-ce que Python?",
        "Donne-moi un nombre aléatoire entre 1 et 100.",
        "Écris un haiku sur l'automne."
    ]
    
    print("\n" + "📚 TEST AVEC PLUSIEURS QUESTIONS ".center(70, "=") + "\n")
    
    for i, question in enumerate(questions, 1):
        print(f"\n{'─'*70}")
        print(f"Question {i}: {question}")
        print('─'*70)
        
        metrics = client.generate(question)
        if metrics:
            print(f"Réponse: {metrics.response}")
            print(f"Temps: {metrics.total_duration:.2f}s")


def exemple_temperature():
    """Compare différentes températures (créativité)"""
    client = OllamaClient()
    prompt = "Invente un nom pour un robot."
    
    print("\n" + "🌡️  TEST DES TEMPÉRATURES ".center(70, "=") + "\n")
    
    for temp in [0.3, 0.7, 1.0]:
        print(f"\n{'─'*70}")
        print(f"Température: {temp} (0=précis, 1=créatif)")
        print('─'*70)
        
        metrics = client.generate(prompt, temperature=temp)
        if metrics:
            print(f"Nom généré: {metrics.response}")


# Pour lancer les exemples supplémentaires, décommente:
# exemple_questions_multiples()
# exemple_temperature()