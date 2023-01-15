import requests
from dotenv import load_dotenv
import os

class DataManager:
    def __init__(self):
        self.destination_data = {}
        
    def get_destination_data(self):
        load_dotenv()
        self.shetty_endpoint = f"https://api.sheety.co/{os.getenv('USERNAME')}/flightDeals/prices"
        self.headers_sheet = {
            "Authorization": f"Bearer {os.getenv('BEARER_TOKEN')}"
        }
        response = requests.get(self.shetty_endpoint, headers=self.headers_sheet)
        response.raise_for_status()
        self.destination_data = response.json()["prices"]
        return self.destination_data
    
    def update_destination_codes(self):
        for city in self.destination_data:
            new_data = {
                "price": {
                    "iataCode": city["iataCode"]
                }
            }
            response = requests.put(
                url=f"{self.shetty_endpoint}/{city['id']}",
                json=new_data,
                headers=self.headers_sheet
            )
            print(response.text)
            
    def get_customer_emails(self):
        customers_endpoint = f"https://api.sheety.co/{os.getenv('USERNAME')}/flightDeals/users"
        response = requests.get(customers_endpoint, headers=self.headers_sheet)
        data = response.json()
        self.customer_data = data["users"]
        return self.customer_data