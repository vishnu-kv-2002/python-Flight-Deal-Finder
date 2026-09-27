from pprint import pprint
from datetime import datetime, timedelta
from data_manager import DataManager
from flight_search import FlightSearch
from flight_data import find_cheapest_flight
from notification_manager import NotificationManager


# ---- 1. Load destination data from Sheety ----
data_manager = DataManager()
sheet_data = data_manager.get_destination_data()
pprint(sheet_data)


# ---- 2. Date range: tomorrow to ~6 months out ----
tomorrow = datetime.now() + timedelta(days=1)
six_month_from_today = datetime.now() + timedelta(days=6 * 30)


# ---- 3. Set up services ----
ORIGIN_CITY_IATA = "CCJ"
flight_search = FlightSearch()
notification_manager = NotificationManager()


# ---- 4. Loop over every destination in the sheet ----
for destination in sheet_data:
    city = destination.get("city", "Unknown")
    iata = destination.get("iataCode")
    lowest_sheet_price = destination.get("lowestPrice")

    if not iata:
        print(f"Skipping {city} — no IATA code in sheet.")
        continue

    if not isinstance(lowest_sheet_price, (int, float)):
        print(f"Skipping {city} — lowestPrice is not a number: {lowest_sheet_price!r}")
        continue

    print(f"\nGetting flights for {city} ({iata})...")
    flights = flight_search.check_flights(
        origin_city_code=ORIGIN_CITY_IATA,
        destination_city_code=iata,
        from_time=tomorrow,
        to_time=six_month_from_today,
    )

    cheapest_flight = find_cheapest_flight(flights, return_date="N/A")
    print(f"{city}: ₹{cheapest_flight.price}")

    if (
        cheapest_flight.price != "N/A"
        and isinstance(cheapest_flight.price, (int, float))
        and cheapest_flight.price < lowest_sheet_price
    ):
        print(f"✅ Lower price flight found to {city}!")

        # Send notification FIRST, then update sheet
        try:
            notification_manager.send_whatsapp(
                message_body=(
                    f"Low price alert! Only ₹{cheapest_flight.price} to fly "
                    f"from {cheapest_flight.origin_airport} "
                    f"to {cheapest_flight.destination_airport} "
                    f"on {cheapest_flight.out_date}."
                )
            )
        except Exception as e:
            print(f"WhatsApp send failed: {e}")

        data_manager.update_lowest_price(destination["id"], cheapest_flight.price)
    else:
        print(f"No cheaper deal for {city} (sheet: ₹{lowest_sheet_price}).")