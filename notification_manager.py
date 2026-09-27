from twilio.rest import Client
import os
from dotenv import load_dotenv

load_dotenv()

class NotificationManager:

    def __init__(self):
        self.client = Client(os.getenv('ACCOUNT_SID'), os.getenv('AUTH_TOKEN'))

    def send_whatsapp(self, message_body):
        message = self.client.messages.create(
            from_='whatsapp:+14155238886',
            body=message_body,
            to='whatsapp:+919778311669'
        )
        # Prints if successfully sent.
        print(message.sid)

