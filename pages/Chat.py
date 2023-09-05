from classes.chat import Chat

import streamlit as st

st.title("Application de discussion")

chat = Chat()

model = st.radio("Modèle", options=('gpt-3.5-turbo', 'gpt-4'))

input_text = st.text_area(label="Posez une question")
if st.button("Envoyer") and input_text:
    chat._add_user_message(input_text)
    response = chat._generate_response(model, input_text)
    
chat._conversation_interface()
