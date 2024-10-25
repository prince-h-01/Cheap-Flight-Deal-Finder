import requests
from datetime import datetime, timedelta
from pprint import pprint

from flight_search import FlightSearch
flight_search = FlightSearch()
from notification_manager import NotificationManager
notification_manager = NotificationManager()

DEPARTURE_CITY_IATA = "LON"

shetty_api_endpoint = "https://api.sheety.co/0cfe9f899c4a047b320ac1366d85738e/myFlightDeals/prices"
response = requests.get(url=shetty_api_endpoint)
result = response.json()
sheet_data = result["prices"]  # holding spreadsheet data in this variable
# pprint(sheet_data)


# 👇👇👇👇👇👇👇👇👇👇👇👇This part inputs IATA CODES in spreadsheet for your desired city
if sheet_data[0]["iataCode"] == "":
    for row in sheet_data:  # each row is a dictionary
        row_number = int(row["id"])
        city_name = row["city"]
        update_data = {
            "price": {
                "iataCode": flight_search.get_destination_code(city_name)
            }
        }

        new_response = requests.put(
            url=f"https://api.sheety.co/0cfe9f899c4a047b320ac1366d85738e/myFlightDeals/prices/{row_number}",
            json=update_data)

# 👆👆👆👆👆👆👆👆👆👆👆👆👆👆👆👆👆👆👆👆👆👆👆👆👆👆👆👆

# Get tomorrow's date
tomorrow = datetime.now().date() + timedelta(days=1)
# Add 6 months to tomorrow's date
six_months_later = tomorrow + timedelta(days=6 * 30)

for row in sheet_data:
    flight_search.get_flight_data(departure_city_iata=DEPARTURE_CITY_IATA,
                                  destination_city_iata=row["iataCode"],
                                  date_from=tomorrow,
                                  date_to=six_months_later)
    if flight_search.price <= row["lowestPrice"]:
        contents = f"Hi Dear,\n\nAir-ticket Price: {flight_search.price}{flight_search.currency}," \
                   f"\nDeparture city name: {flight_search.departure_city_name}," \
                   f"\nDeparture airport IATA code: {flight_search.departure_airport_iata_code}," \
                   f"\nArrival city name: {flight_search.arrival_city_name}," \
                   f"\nArrival airport IATA code: {flight_search.arrival_airport_iata_code}," \
                   f"\nDeparture Date: {flight_search.departure_date}," \
                   f"\nReturn Date: {flight_search.return_date}" \
                   f"\nBuying Link: {flight_search.buying_link}"

        notification_manager.send_email(contents=contents)
