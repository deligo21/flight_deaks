from pprint import pprint
from data_manager import DataManager
from flight_search import FlightSearch
from datetime import datetime, timedelta
from notification_manager import NotificationManager

data_manager = DataManager()
sheet_data = data_manager.get_destination_data()
flight_search = FlightSearch()


ORIGIN_CITY_IATA = "LON"

if sheet_data[0]["iataCode"] == "":
    flight_search = FlightSearch()
    for row in sheet_data:
        row["iataCode"] = flight_search.get_destination_code(row["city"])
    pprint(f"sheet_data:\n {sheet_data}")

    data_manager.destination_data = sheet_data
    data_manager.update_destination_codes()
    
tomorrow = datetime.now() + timedelta(days=1)
six_month_from_today = datetime.now() + timedelta(days=(6 * 30))

for destination in sheet_data:
    flight = flight_search.check_flights(
        ORIGIN_CITY_IATA,
        destination["iataCode"],
        from_time=tomorrow,
        to_time=six_month_from_today
    )
    if flight != None:
        if flight.price < destination["lowestPrice"]:
            
            users = data_manager.get_customer_emails()
            emails = [row["email"] for row in users]
            names = [row["firstName"] for row in users]
            
            notification = NotificationManager(flight.price, flight.origin_city, flight.origin_airport, flight.destination_city, flight.destination_airport, flight.out_date, flight.return_date)
            
            if flight.stop_overs > 0:
                notification.bot_message += f"\nFlight has {flight.stop_overs} stop over, via {flight.via_city}."

            link = f"https://www.google.co.uk/flights?hl=en#flt={flight.origin_airport}.{flight.destination_airport}.{flight.out_date}*{flight.destination_airport}.{flight.origin_airport}.{flight.return_date}"
            notification.telegram_bot_sendtext()
            notification.send_emails(emails, notification.bot_message, link)
            

# print("Welcome to Rodrigo's Flight Club\nWe find the best flight deals and email you.")
# name = input("What is your first name?\n")
# last_name = input("What is your last name?\n")
# email = input("What is your email?\n")
# email_again = input("Type your email again.\n")

# if email == email_again:
#     print("Succss! Welcome to the club :D")
# else:
#     print('Try again')