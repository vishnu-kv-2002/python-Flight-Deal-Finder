# ✈️ Flight Deal Finder

A Python flight deal finder that searches for low-cost flights from a selected origin airport to multiple destinations. It gets destination information from a Google Sheet, searches for available flights using Google Flights through SerpApi, compares prices with the saved lowest prices, and sends a WhatsApp notification when a cheaper flight is found.

## 🚀 Features

* ✈️ Searches for flights between multiple destinations
* 📊 Reads destination and target prices from Google Sheets
* 🔎 Searches Google Flights using SerpApi
* 💰 Finds the cheapest available flight
* 📉 Compares current flight prices with saved lowest prices
* 📱 Sends WhatsApp notifications using Twilio
* 📝 Updates the lowest price in the Google Sheet
* 🔐 Uses environment variables for API credentials
* 🧩 Uses separate Python classes for different parts of the application

## 🛠️ Technologies Used

* Python
* Requests
* SerpApi
* Google Flights
* Sheety API
* Google Sheets
* Twilio
* WhatsApp
* python-dotenv

## 📁 Project Structure

```text
Flight-Deal-Finder/
│
├── main.py
├── data_manager.py
├── flight_search.py
├── flight_data.py
├── notification_manager.py
├── requirements.txt
├── .env
├── .gitignore
└── README.md
```

## 📦 Installation

Install the required packages:

```bash
pip install -r requirements.txt
```

Your `requirements.txt` should contain:

```text
requests
twilio
python-dotenv
```

`os`, `datetime`, and other standard Python modules do not need to be included in `requirements.txt`.

## 🔐 Environment Variables

Create a `.env` file in the project directory:

```env
SERPAPI_KEY=your_serpapi_key

SHEET_USER=your_sheety_username
SHEET_PASSWORD=your_sheety_password

ACCOUNT_SID=your_twilio_account_sid
AUTH_TOKEN=your_twilio_auth_token
```

The program loads these values using `python-dotenv`.

### ⚠️ Security

Never upload your `.env` file or API credentials to GitHub.

Add this to `.gitignore`:

```gitignore
.env
```

If any real API keys or credentials have already been exposed publicly, revoke or regenerate them.

## 📊 Google Sheet

The project uses a Google Sheet to store destination information and the lowest prices.

Example:

| City   | IATA Code | Lowest Price |
| ------ | --------- | -----------: |
| London | LON       |       ₹50000 |
| Paris  | PAR       |       ₹45000 |
| Dubai  | DXB       |       ₹20000 |

The program reads these values and searches for flights to each destination.

## ⚙️ How It Works

### 1. Load Destination Data

`DataManager` gets destination information from the Sheety API.

```python
sheet_data = data_manager.get_destination_data()
```

The data contains the destination city, IATA code, and saved lowest price.

### 2. Set the Search Period

The program searches from:

* Tomorrow
* Up to approximately six months from the current date

```python
tomorrow = datetime.now() + timedelta(days=1)
six_month_from_today = datetime.now() + timedelta(days=6 * 30)
```

### 3. Search for Flights

The origin airport is set to:

```text
CCJ
```

The program searches for one-way flights from the origin to each destination.

### 4. Find the Cheapest Flight

`find_cheapest_flight()` checks the flight results and finds the flight with the lowest price.

It searches through:

* Best flights
* Other flights

The cheapest result is stored in a `FlightData` object.

### 5. Compare Prices

The current flight price is compared with the lowest price stored in the Google Sheet.

If the current price is lower:

```text
Current price < Saved lowest price
```

the program identifies it as a lower-price deal.

### 6. Send WhatsApp Notification

When a cheaper flight is found, the program sends a WhatsApp message using Twilio.

Example:

```text
Low price alert! Only ₹18500 to fly
from CCJ to DXB
on 2026-10-15.
```

### 7. Update the Google Sheet

After the notification attempt, the new lowest price is saved back to the Google Sheet.

## 🧩 Main Components

### `main.py`

Acts as the main controller of the application.

It:

* Loads destination data
* Sets the date range
* Searches flights
* Finds the cheapest flight
* Compares prices
* Sends notifications
* Updates the sheet

### `data_manager.py`

Handles communication with the Sheety API.

Main responsibilities:

* Retrieve destination data
* Update the lowest flight price

### `flight_search.py`

Handles flight searches using SerpApi.

It sends:

* Origin airport
* Destination airport
* Departure date
* Number of passengers
* Currency

and returns the flight search results.

### `flight_data.py`

Contains the `FlightData` class and the `find_cheapest_flight()` function.

It processes the flight results and identifies the cheapest flight.

### `notification_manager.py`

Handles WhatsApp notifications using Twilio.

It creates and sends the WhatsApp message when a cheaper flight is found.

## 🧠 Concepts Learned

* Object-oriented programming
* Python classes
* Working with APIs
* REST API requests
* GET and PUT requests
* JSON data
* API authentication
* HTTP Basic Authentication
* Environment variables
* `python-dotenv`
* Working with dates and `timedelta`
* Exception handling
* Lists and dictionaries
* Searching for minimum values
* Modular Python project structure
* WhatsApp automation

## ▶️ How to Run

After setting up your `.env` file, run:

```bash
python main.py
```

The program will:

```text
Load destinations
        ↓
Search flights
        ↓
Find cheapest flight
        ↓
Compare with saved price
        ↓
Cheaper price found?
      ↙       ↘
    YES        NO
     ↓          ↓
WhatsApp     Continue
 alert
     ↓
Update Google Sheet
```

## 🔮 Future Improvements

* Search both one-way and round-trip flights
* Add departure and return dates
* Support multiple origin airports
* Add airline information to notifications
* Include flight duration in the alert
* Add stop/layover information
* Run the program automatically every day
* Add email notifications
* Add a graphical dashboard
* Allow users to configure destinations through a GUI

## 👨‍💻 Author

**Vishnu K V**

A Python automation project created to practice API integration, object-oriented programming, flight-price comparison, Google Sheets integration, and WhatsApp notifications.
