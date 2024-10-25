import requests

flight_search_end_point = "https://api.tequila.kiwi.com/v2/search"
TEQUILA_API_KEY = "7EvfakZyf5fqSRpIcv8ZXpZfpdhA_779"
CURRENCY = "GBP"


class FlightSearch:

    def __init__(self):
        self.price = 0
        self.departure_city_name = ""
        self.departure_airport_iata_code = ""
        self.arrival_city_name = ""
        self.arrival_airport_iata_code = ""
        self.departure_date = ""
        self.return_date = ""
        self.buying_link = ""
        self.currency = ""

    def get_destination_code(self, city_name):

        headers = {
            "apikey": TEQUILA_API_KEY
        }

        params = {
            'term': city_name,
            'location_types': 'airport'
        }

        response = requests.get(url="https://api.tequila.kiwi.com/locations/query", params=params, headers=headers)
        result = response.json()
        code = result["locations"][0]["city"]["code"]
        return code

    def get_flight_data(self, departure_city_iata, destination_city_iata, date_from, date_to):

        headers = {
            "apikey": TEQUILA_API_KEY
        }
        parameters_query = {
            "fly_from": departure_city_iata,
            "fly_to": destination_city_iata,
            "date_from": date_from.strftime("%d/%m/%Y"),
            "date_to": date_to.strftime("%d/%m/%Y"),
            "nights_in_dst_from": 7,
            "nights_in_dst_to": 28,
            "max_stopovers": 0,  # for direct flight
            "curr": CURRENCY,
            "flight_type": "round",
            "sort": "price",
            "one_for_city": 1  # returns the cheapest price

        }
        response = requests.get(url=flight_search_end_point, params=parameters_query, headers=headers)

        # this exception handling handles if there is no flight on that date. This can happen due to Very Bad Weather etc
        try:
            data = response.json()["data"][0]
        except IndexError:
            print(f"No flights found for {destination_city_iata}.")
            return None

        cheapest_price = data["price"]

        self.price = cheapest_price
        self.departure_city_name = data["cityFrom"]
        self.departure_airport_iata_code = data["flyFrom"]
        self.arrival_city_name = data["cityTo"]
        self.arrival_airport_iata_code = data["flyTo"]
        self.departure_date = data["route"][0]["utc_departure"]
        self.return_date = data["route"][1]["utc_departure"]
        self.buying_link = data["deep_link"]
        self.currency = response.json()["currency"]



