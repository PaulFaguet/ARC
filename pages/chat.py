import openai
import streamlit as st
import threading


st.warning("Merci de ne pas abuser du modèle GPT-4. Son quotas est de 50 messages toutes les 4 heures.")

# create a variable thath rests itself every 4 hours
if 'quotas' not in st.session_state:
    st.session_state.quotas = 0
    
def reset_quotas(quotas):
    st.session_state.quotas = 0
    
threading.Timer(4*60*60, reset_quotas).start()
st.info(f"Quotas actuels : {st.session_state.quotas}")

model_selector = st.selectbox(options=('gpt-3.5-turbo', 'gpt-4'), label='Model')
if 'messages' not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are a helpful assistant."}
    ]

input = st.text_input(label='Input')
ask = st.button('Ask')
if ask:
    st.session_state.messages.append({"role": "user", "content": input})
    
    resp = openai.ChatCompletion.create(
        model=model_selector,
        messages=st.session_state.messages
    )
    resp = resp['choices'][0]['message']['content']
    st.session_state.messages.append({"role": "system", "content": resp})
    st.session_state.quotas += 1
    st.write(resp)
    
import datetime
start_date = '2022-11-22'

# add 30 days to the date
new_date = (datetime.datetime.strptime(start_date, '%Y-%m-%d') + datetime.timedelta(days=31)).strftime('%Y-%m-%d')
new_date
date_test = datetime.datetime.strptime(new_date, '%Y-%m-%d') + datetime.timedelta(days=30)
date_test = date_test.strftime('%Y-%m-%d')
date_test = datetime.datetime.strptime(date_test, '%Y-%m-%d') + datetime.timedelta(days=30)
date_test = date_test.strftime('%Y-%m-%d')
date_test = datetime.datetime.strptime(date_test, '%Y-%m-%d') - datetime.timedelta(days=30)
date_test = date_test.strftime('%Y-%m-%d')

