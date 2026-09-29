import streamlit as st
import requests


# Adresse de l'API FastAPI
FASTAPI_URL = "http://127.0.0.1:8000/generate-email"


# Configuration de la page
st.set_page_config(
    page_title="Assistant IA Courriels",
    page_icon="📧",
    layout="wide"
)

# titre de la page
st.title("📧 Assistant IA de rédaction de courriels")


# --------------------------------------------------
# Informations du courriel
# --------------------------------------------------

col1, col2 = st.columns(2)


with col1:

# destinataire du courriel
# une liste déroulante avec les options suivantes : Direction Générale, Sous-direction, Gestionnaire, Un autre employé, Diffusion générale, Un autre service
    destinataire = st.selectbox(
        "Destinataire",
        [
            "Direction Générale",
            "Sous-direction",
            "Gestionnaire",
            "Un autre employé",
            "Diffusion générale",
            "Un autre service"
        ]
    )


with col2:
# style du courriel
# une liste déroulante avec les options suivantes : Concis, Précis, Résumé, Développé, Détaillé, Complet, Exhaustif
    style = st.selectbox(
        "Style de format",
        [
            "Concis",
            "Précis",
            "Résumé",
            "Développé",
            "Détaillé",
            "Complet",
            "Exhaustif"
        ]
    )


col3, col4 = st.columns(2)
# type de courriel
# une liste déroulante avec les options suivantes : Demande d'information, Note pour les directions, Rapport d'analyse ou de synthèse, Invitation, Relance, Remerciement
with col3:

    type_courriel = st.selectbox(
        "Type de courriel",
        [
            "Demande d'information",
            "Note pour les directions",
            "Rapport d'analyse ou de synthèse",
            "Invitation",
            "Relance",
            "Remerciement"
        ]
    )
# ton du courriel
# une liste déroulante avec les options suivantes : Professionnel, Très formel, Amical, Commercial

with col4:

    ton = st.selectbox(
        "Ton",
        [
            "Professionnel",
            "Très formel",
            "Amical",
            "Commercial"
        ]
    )


# --------------------------------------------------
# Contexte
# --------------------------------------------------
# liste déroulante avec les options suivantes : Contexte, Détails, Informations supplémentaires
contexte = st.text_area(
    "Informations à joindre au courriel (contexte, détails, etc.)",
    height=200
)


# --------------------------------------------------
# Génération
# --------------------------------------------------
# un bouton pour générer le courriel
# envoie les informations à FastAPI pour générer le courriel

if st.button(
    "✨ Générer le courriel",
    use_container_width=True
):
# le contexte ne doit pas être vide, sinon afficher un message d'avertissement
    if not contexte.strip():

        st.warning(
            "Veuillez saisir un contexte."
        )

    else:
# les autres champs ne doivent pas être vides, sinon afficher un message d'avertissement
        # Données envoyées à FastAPI
        payload = {
            "destinataire": destinataire,
            "style": style,
            "type_courriel": type_courriel,
            "ton": ton,
            "contexte": contexte
        }

# Afficher un spinner pendant la génération du courriel
        with st.spinner("Génération en cours..."):

            try:

                response = requests.post(
                    FASTAPI_URL,
                    json=payload,
                    timeout=60
                )

# extraire le courriel de la réponse FastAPI
                # Vérification de la réponse
                if response.status_code == 200:

                    email = response.text

                    # Séparer l'objet du reste
                    parties = email.split("\n\n", 1)

                    # objet = parties[0].strip()
                    reste = parties[1].strip() if len(parties) > 1 else ""

                    # Séparer les salutations du corps
                    parties_corps = reste.split("\n\n", 1)

                    # salutations = parties_corps[0].strip() if len(parties_corps) > 0 else ""
                    corps = parties_corps[1].strip() if len(parties_corps) > 1 else ""

                    st.session_state["email"] = email

                else:

                    st.error(
                        f"Erreur FastAPI : "
                        f"{response.status_code}\n\n"
                        f"{response.text}"
                    )

            except requests.exceptions.ConnectionError:

                st.error(
                    "Impossible de contacter FastAPI. "
                    "Vérifiez que le serveur FastAPI est démarré "
                    "sur le port 8000."
                )

            except requests.exceptions.Timeout:

                st.error(
                    "Le serveur FastAPI a mis trop de temps à répondre."
                )

            except Exception as e:

                st.error(
                    f"Erreur : {e}"
                )


# --------------------------------------------------
# Affichage du courriel
# --------------------------------------------------

if "email" in st.session_state:

    st.subheader("📨 Courriel généré")


    st.text_area(
        "Contenu",
        value=st.session_state["email"],
        height=350
    )


    st.download_button(
        label="📥 Télécharger",
        data=st.session_state["email"],
        file_name="courriel.txt",
        mime="text/plain"
    )