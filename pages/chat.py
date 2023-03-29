import openai
import streamlit as st


st.write('https://platform.openai.com/docs/guides/chat/introduction')

model_selector = st.selectbox(options=('gpt-3.5-turbo', 'gpt-4'), label='Model')
input = st.text_input(label='Input')
# resp = openai.ChatCompletion.create(
# #   model="gpt-3.5-turbo",
#     model='gpt-4',
#     messages=[
#             {"role": "system", "content": "You are a helpful assistant."},
#             {"role": "user", "content": "Who won the world series in 2020?"},
#             {"role": "assistant", "content": "The Los Angeles Dodgers won the World Series in 2020."},
#             {"role": "user", "content": "Where was it played?"}
#         ]
# )
# st.write(resp['choices'][0]['message']['content'])