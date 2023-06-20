import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header
from email.mime.application import MIMEApplication
import streamlit as st

def send_email(sender, password, receiver, smtp_server, 
    smtp_port, email_message, subject, attachment=None):
    message = MIMEMultipart()
    message['To'] = Header(receiver)
    message['From']  = Header(sender)
    message['Subject'] = Header(subject)
    message.attach(MIMEText(email_message,'plain', 'utf-8'))
    st.write('OK 1')
    
    if attachment:
        att = MIMEApplication(attachment.read(), _subtype="txt")
        att.add_header('Content-Disposition', 'attachment', filename=attachment.name)
        message.attach(att)
    st.write('OK 2')
        
        
    server = smtplib.SMTP(smtp_server, smtp_port)
    st.write('OK 3')
    # server.starttls()
    st.write('OK 4')
    server.ehlo()
    st.write('OK 5')
    # server.login(sender, password)
    st.write('OK 6')
    text = message.as_string()
    server.sendmail(sender, receiver, text)
    st.write('OK 7')
    print('E-mail envoyé avec succès !')
    server.quit()
    
st.header('Envoi d\'e-mail')

if st.button('Envoyer'):
    try:
        send_email('monitoring-adcom@axess.fr', 'Fp27dVM35Cnm', 
                'paul.faguet@axess.fr', 'smtp.axess.fr', 25, 'Test', 'Test'
                'temp_result.txt')
        st.success('E-mail envoyé avec succès !')
    except Exception as e:
        st.error(f'Erreur lors de l\'envoi de l\'e-mail : {e}')