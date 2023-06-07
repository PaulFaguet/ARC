import json
import openai
import streamlit as st

class Chat:
    def __init__(self):
        self.messages = [
            {"role": "system", "content": "Tu es un assistant SEO utile."}
        ]
        self._load_messages()
        
    def _load_messages(self):
        if "messages" in st.session_state:
            self.messages = st.session_state.messages
    
    def _save_messages(self):
        st.session_state.messages = self.messages
    
    def _add_user_message(self, content):
        self.messages.append({"role": "user", "content": content})
        self._save_messages()
    
    def _add_assistant_message(self, content):
        self.messages.append({"role": "system", "content": content})
        self._save_messages()
    
    def _conversation_interface(self):
        for message in reversed(self.messages):
            if message['role'] == 'user':
                st.info(f"Vous : {message['content']}")
            elif message['role'] == 'assistant':
                st.success(f":robot_face: : {message['content']}")

    
    def _generate_response(self, model: str, prompt: str):
       # Chargement des messages existants
        messages = self.messages.copy()

        # Ajout du nouveau message de l'utilisateur
        messages.append({"role": "user", "content": prompt})

        # Appel à OpenAI pour générer la réponse de l'assistant
        completion = openai.ChatCompletion.create(
            model=model,
            messages=messages
        )

        # Récupération de la réponse générée par l'assistant
        assistant_message = completion.choices[0].message.content

        # Ajout de la réponse de l'assistant aux messages
        assistant_response = {"role": "assistant", "content": assistant_message}
        self.messages.append(assistant_response)
        self._save_messages()

        return assistant_message

    def _export_to_json(self):
        with open("conversation.json", 'w') as file:
            json.dump(self.messages, file, indent=4)
        
        
        