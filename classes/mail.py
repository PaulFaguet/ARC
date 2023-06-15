import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
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

    def _creer_message(self):
        message = MIMEMultipart()
        message['From'] = self.sender
        message['To'] = self.mail
        message['Subject'] = f"Résultats ARC - {self.object}"
        
        content = f"Vous troouverez ci-joint les résultats concernant {self.object}"
        message.attach(MIMEText(content, 'plain'))
        
        return message

    def _ajouter_piece_jointe(self, message):
        attachment = MIMEBase('application', 'octet-stream')
        attachment.set_payload(open('temp_result.txt', 'rb').read())
        encoders.encode_base64(attachment)
        attachment.add_header('Content-Disposition', "attachment; filename=ARC_result.txt")
        message.attach(attachment)

    def _envoyer_message(self, message):
        with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
            server.send_message(message)

    def run(self):
        message = self._creer_message()
        self._ajouter_piece_jointe(message)
        self._envoyer_message(message)
        
        print("E-mail envoyé avec succès !")