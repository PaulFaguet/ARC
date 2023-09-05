import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.header import Header
from email import encoders
import os
from dotenv import load_dotenv

load_dotenv()

class Mail:
    def __init__(self, mail: str, mail_object: str):
        self.mail = mail
        self.object = mail_object
        
        self.smtp_server = os.getenv('TNR_SMTP_AXESS')
        self.smtp_port = os.getenv('TNR_PORT_MAIL')
        self.sender = os.getenv('TNR_USER_AXESS')

    def send_email(self):
        message = MIMEMultipart()
        
        message['From'] = Header(self.sender)
        message['To'] = Header(self.mail)
        message['Subject'] = Header(f"Résultats ARC - {self.object}")
        
        content = f"Vous troouverez ci-joint les résultats concernant {self.object}"

        message.attach(MIMEText(content, 'plain', 'utf-8'))
        attachment = open('temp_result.txt', 'rb')
        att = MIMEApplication(attachment.read(), _subtype="txt")
        att.add_header('Content-Disposition', 'attachment', filename=attachment.name)
        message.attach(att)
        server = smtplib.SMTP(self.smtp_server, self.smtp_port)
        # server.starttls()
        # server.ehlo()
        # server.login('monitoring-adcom@axess.fr', 'Fp27dVM35Cnm')
        text = message.as_string()
        server.sendmail('monitoring-adcom@axess.fr', self.mail, text)
        server.quit()
        
        print('E-mail envoyé avec succès !')
    
    # def _creer_message(self):
    #     message = MIMEMultipart()
    #     message['From'] = Header(self.sender)
    #     message['To'] = Header(self.mail)
    #     message['Subject'] = Header(f"Résultats ARC - {self.object}")
        
    #     content = f"Vous troouverez ci-joint les résultats concernant {self.object}"
    #     message.attach(MIMEText(content, 'plain'))
        
    #     return message

    # def _ajouter_piece_jointe(self, message):
    #     attachment = MIMEApplication('application', 'octet-stream')
    #     attachment.set_payload(open('temp_result.txt', 'rb').read())
    #     encoders.encode_base64(attachment)
    #     attachment.add_header('Content-Disposition', "attachment; filename=ARC_result.txt")
    #     message.attach(attachment)
        
    #     return message

    # def _envoyer_message(self, message):
    #     with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
    #         server.sendmail(self.sender, self.mail, message.as_string())
    #         server.quit()

    # def run(self):
    #     message = self._creer_message()
    #     self._ajouter_piece_jointe(message)
    #     self._envoyer_message(message)
        
    #     print("E-mail envoyé avec succès !")

mail = Mail('paul.faguet@axess.fr', 'test')
mail.send_email()