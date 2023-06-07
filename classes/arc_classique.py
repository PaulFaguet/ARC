import pandas as pd
import openai

class ARC_Classique:
    def __init__(self):
        self.df_examples = pd.read_json('classes\prompt_examples.json')
        
    def create_prompt(self, user_text_input: str, user_word_number_input: int):
        prompt = f"{user_text_input}. Tu es un rédacteur dans une agence de référencement web qui rédige des textes pour soigner le SEO. Le texte se doit d'être intelligible et de respecter les consignes fournies ci-dessus. Le texte doit être d'environ {user_word_number_input} mots."
        return prompt
    
    def generate_answer(self, user_text_input: str, user_word_number_input: int, user_temperature_input: int):
        response = openai.Completion.create(
            engine = 'text-davinci-003',
            prompt = self.create_prompt(user_text_input, user_word_number_input),
            temperature = user_temperature_input,
            max_tokens = 2000,
        )

        return response['choices'][0]['text']