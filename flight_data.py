class FlightData:

    def __init__(self, price, origin_airport, destination_airport, out_date, return_date):
        self.price = price
        self.origin_airport = origin_airport
        self.destination_airport = destination_airport
        self.out_date = out_date
        self.return_date = return_date


def find_cheapest_flight(data, return_date="N/A"):
    # No data at all
    if data is None or (not data.get("best_flights") and not data.get("other_flights")):
        print("No flight data")
        return FlightData("N/A", "N/A", "N/A", "N/A", return_date)

    all_flights = data.get("best_flights", []) + data.get("other_flights", [])

    # These lines set up a starting point before checking flights: the first creates an empty placeholder
    # flight with no real data yet, and the second sets the "lowest price so far"
    # to infinity, so the very first real flight price found will automatically replace it.
    cheapest_flight = FlightData("N/A", "N/A", "N/A", "N/A", return_date)
    lowest_price = float("inf")

    for flight in all_flights:
        price = flight.get("price")
        if price is None:
            print("--- No price available for flight. ---")
            continue

        if price < lowest_price:
            try:
                origin = flight["flights"][0]["departure_airport"]["id"]
                destination = flight["flights"][-1]["arrival_airport"]["id"]
                out_date = flight["flights"][0]["departure_airport"]["time"].split(" ")[0]
            except (KeyError, IndexError) as e:
                print(f"Skipping malformed flight entry: {e}")
                continue

            lowest_price = price
            cheapest_flight = FlightData(
                price, origin, destination, out_date, return_date
            )
            print(f"New lowest: {origin} → {destination} ₹{price} on {out_date}")

    return cheapest_flight