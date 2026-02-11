import streamlit as st
from openai import OpenAI
import os
import yaml

# -------- CLÉ API -------- #
# client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

# -------- CHARGEMENT DU CV -------- #
def load_cv(filename="cv.yaml"):
    with open(filename, "r", encoding="utf-8") as file:
        data = yaml.safe_load(file)
    return data

def format_cv(data):
    """Convertit le YAML en texte lisible pour l'IA"""
    texte = ""
    for section, contenu in data.items():
        texte += f"{section}:\n"
        if isinstance(contenu, list):
            for item in contenu:
                if isinstance(item, dict):
                    for key, value in item.items():
                        if isinstance(value, list):
                            texte += f"  {key}: " + ", ".join(value) + "\n"
                        else:
                            texte += f"  {key}: {value}\n"
                else:
                    texte += f"  - {item}\n"
        else:
            texte += f"  {contenu}\n"
        texte += "\n"
    return texte

cv_data = load_cv()
CV = format_cv(cv_data)

# -------- PROMPT SYSTÈME -------- #
SYSTEM_PROMPT = f"""
Tu es un assistant professionnel chargé de répondre aux recruteurs.
Ton rôle : mettre en valeur le profil de Marie Fournigault.
Réponds uniquement aux questions professionnelles.
Si une question est personnelle (âge, salaire, situation familiale, adresse, religion, etc), réponds :
"Je préfère me concentrer sur les éléments professionnels du profil."
Sois synthétique, clair et honnête.

Voici le profil :
{CV}
"""

# -------- FONCTION CHAT -------- #
def ask_ai(messages):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        temperature=0.4
    )
    return response.choices[0].message.content

# -------- INTERFACE STREAMLIT -------- #
st.set_page_config(
    page_title="CV interactif - Marie Fournigault",
    page_icon="💬",
    layout="centered"
)

st.title("💬 CV interactif")
st.write("Posez une question sur mon parcours professionnel.")

# Mémoire de conversation
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": SYSTEM_PROMPT}]

# Affichage de l'historique
for msg in st.session_state.messages[1:]:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# Input utilisateur
if prompt := st.chat_input("Votre question..."):
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        response = ask_ai(st.session_state.messages)
        st.write(response)

    st.session_state.messages.append({"role": "assistant", "content": response})
