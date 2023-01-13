import requests
from dotenv import load_dotenv
import os

class NotificationManager:
    
    def __init__(self, price, departure_city, departure_airport,arrival_city,arrival_airport, outbound_date, inbound_date):
        self.price = price
        self.departure_city = departure_city
        self.departure_airport = departure_airport
        self.arrival_city = arrival_city
        self.arrival_airport = arrival_airport
        self.outbound_date = outbound_date
        self.inbound_date = inbound_date
    
    def telegram_bot_sendtext(self):
        
        bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
        bot_chatID = os.getenv('CHAT_ID')
        
        bot_message = f"Low price alert :P!\nOnly £{self.price} to fly from {self.departure_city}-{self.departure_airport} to {self.arrival_city}-{self.arrival_airport},\nfrom {self.outbound_date} to {self.inbound_date}"
        
        send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message

        response = requests.get(send_text)

        return response.json()