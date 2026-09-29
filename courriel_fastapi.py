from fastapi import FastAPI
from pydantic import BaseModel
import os

from openai import OpenAI

# --------------------------------------------------
# Configuration
# --------------------------------------------------

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:

    raise ValueError(
        "La variable d'environnement OPENAI_API_KEY "
        "n'est pas définie."
    )

# Client OpenAI
client = OpenAI(
    api_key=OPENAI_API_KEY
)

# Application FastAPI
app = FastAPI()

# --------------------------------------------------
# Modèle des données reçues
# --------------------------------------------------

class EmailRequest(BaseModel):

    destinataire: str
    style: str
    type_courriel: str
    ton: str
    contexte: str

# --------------------------------------------------
# Endpoint
# --------------------------------------------------

@app.post("/generate-email")
async def generate_email(data: EmailRequest):

    # Construction du prompt
    prompt = f"""
    Génère un courriel professionnel en français.

    Voici les informations fournies :

    Destinataire :{data.destinataire}

    Style :{data.style}

    Type de courriel :{data.type_courriel}

    Ton :{data.ton}

    Contexte :{data.contexte}

    Consignes : en utilisant les informations dans le contexte,

    - Redige un objet de courriel approprié.
    - Utilise une formule de salutation.
    - Rédige le contenu du courriel.
    - Termine avec une formule de politesse appropriée selon le destinataire.
    - Respecte le ton, le style, le type de courriel demandé.
    - Retourne uniquement en paragraphes séparés, l'Objet, la salutation et le Corps du message sans signature à la fin. """
# message de prompt pour OpenAI
    message=[
    {
        "role": "system",
        "content": "Tu es un assistant qui rédige des courriels professionnels en français."
    },
    {
        "role": "user",
        "content": prompt
    }]

    # Appel à OpenAI
    response = client.responses.create(
        model="gpt-4o-mini",
        input=message,
        # max_output_tokens=50
    )

    # Texte généré
    email = response.output_text

    # Réponse JSON envoyée à Streamlit
    return email

# --------------------------------------------------
# Lancement du serveur
# --------------------------------------------------

if __name__ == "__main__":

    import uvicorn

    uvicorn.run(
        "courriel_fastapi:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )