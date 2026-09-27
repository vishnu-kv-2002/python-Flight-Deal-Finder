import os
import requests
from requests.auth import HTTPBasicAuth

SHEETY_PRICES_ENDPOINT = (
    'https://api.sheety.co/b759097b2e33c63ef4d4b9e5ef34f12c/flightDeals/prices'
)

class DataManager:

    def __init__(self):
        self._user = os.getenv('SHEET_USER')
        self._password = os.getenv('SHEET_PASSWORD')
        self._authorization = HTTPBasicAuth(self._user, self._password)
        self.destination_data = {}

    def get_destination_data(self):
        response = requests.get(
            url=SHEETY_PRICES_ENDPOINT,
            auth=self._authorization,
        )
        response.raise_for_status()
        data = response.json()
        self.destination_data = data.get('prices', [])
        return self.destination_data

    def update_lowest_price(self, row_id, new_price):
        new_data = {"price": {"lowestPrice": new_price}}
        response = requests.put(
            url=f"{SHEETY_PRICES_ENDPOINT}/{row_id}",
            json=new_data,
            auth=self._authorization,
        )
        if response.status_code not in (200, 201):
            print(f"Sheety update failed: {response.status_code} — {response.text}")
        else:
            print(f"Sheet updated: row {row_id} → ₹{new_price}")