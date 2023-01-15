import requests
from dotenv import load_dotenv
import os
import smtplib

class NotificationManager:
    
    def __init__(self, price, departure_city, departure_airport,arrival_city,arrival_airport, outbound_date, inbound_date):
        self.price = price
        self.departure_city = departure_city
        self.departure_airport = departure_airport
        self.arrival_city = arrival_city
        self.arrival_airport = arrival_airport
        self.outbound_date = outbound_date
        self.inbound_date = inbound_date
        
        load_dotenv()
    
    def telegram_bot_sendtext(self):
        
        bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
        bot_chatID = os.getenv('CHAT_ID')
        
        self.bot_message = f"Low price alert :P!\nOnly £{self.price} to fly from {self.departure_city}-{self.departure_airport} to {self.arrival_city}-{self.arrival_airport},\nfrom {self.outbound_date} to {self.inbound_date}"
        
        send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + self.bot_message

        response = requests.get(send_text)

        return response.json()
    
    def send_emails(self, emails, message, google_flight_link):
        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(os.getenv('MY_EMAIL'), os.getenv('PASSWORD_EMAIL'))
            for email in emails:
                connection.sendmail(
                    from_addr=os.getenv('MY_EMAIL'),
                    to_addrs=email,
                    msg=f"Subject:New Low Price Flight!\n\n{message}\n{google_flight_link}".encode('utf-8')
                )