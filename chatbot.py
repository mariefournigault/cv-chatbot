import os
import streamlit as st
from openai import OpenAI
import yaml



# 🔐 Récupération sécurisée de la clé API
client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

# lire le cv

with open(f'{working_dir}/cv.yaml', 'r', encoding='utf-8') as file:
    cv = yaml.safe_load(file)

# configuring streamlit page settings
st.set_page_config(
    layout="centered"
)

# initialize chat session in streamlit if not already present
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# streamlit page title
st.title("🤖 Bienvenue ! Posez-moi vos questions sur Marie.")

with st.expander('Vous voulez savoir comment je fonctionne ?') :
    st.write("Lorsque vous me posez une question, l'application fait une requête (comprenant le CV de Marie) sur l'API OpenAI, ce qui me permet de vous répondre :)")

# display chat history
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# input field for user's message
user_prompt = st.chat_input("Posez-moi une question...")

if user_prompt:
    # add user's message to chat and display it
    st.chat_message("user").markdown(user_prompt)
    print(f"bot_msg_user : {user_prompt}")
    st.session_state.chat_history.append({"role": "user", "content": user_prompt})

    # send user's message to GPT-4o and get a response
    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": cv_string},
            # unpacking list to append each element on messages list
            *st.session_state.chat_history
        ]
    )

    assistant_response = response.choices[0].message.content
    print(f"bot_msg_assistant : {assistant_response}")
    st.session_state.chat_history.append({"role": "assistant", "content": assistant_response})

    # display GPT-4o's response
    with st.chat_message("assistant"):
        st.markdown(assistant_response)
