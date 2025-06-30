from langchain.tools import tool
from backend.agent.google_calender import block_calendar as real_block_calendar
from backend.agent.amadeus_flight import search_flights
from backend.agent.hotels_rapidapi import get_hotels_in_city
import re
from datetime import datetime, timedelta

@tool
def book_flight(input: str) -> str:
    """
    Book a flight based on user input in the format 'DEL to JFK on 2025-07-20'.
    """
    try:
        print(f"🛬 Received input: {input}")
        if " to " not in input or " on " not in input:
            return "❌ Invalid input format. Use 'DEL to JFK on 2025-07-20'."

        parts = input.split(" on ")
        route = parts[0].split(" to ")
        if len(route) != 2 or len(parts) != 2:
            return "❌ Invalid input format. Use 'DEL to JFK on 2025-07-20'."

        origin = route[0].strip().strip("'\"").upper()
        destination = route[1].strip().strip("'\"").upper()
        date = parts[1].strip().strip("'\"")

        return search_flights(origin, destination, date)
    except Exception as e:
        return f"❌ Failed to book flight: {str(e)}"

@tool
def book_hotel(input: str) -> str:
    """
    Book a hotel in the format: 'City on YYYY-MM-DD for X nights'.
    """
    try:
        if " on " not in input or " for " not in input or " nights" not in input:
            return "❌ Invalid input format. Use 'City on YYYY-MM-DD for X nights'."

        city_part, rest = input.split(" on ")
        date_part, nights_part = rest.split(" for ")
        city = city_part.strip()
        checkin = date_part.strip()
        nights = int(re.sub(r"\D", "", nights_part))  # safely extract numeric part
        checkout = (datetime.strptime(checkin, "%Y-%m-%d") + timedelta(days=nights)).strftime("%Y-%m-%d")

        return get_hotels_in_city(city, checkin, checkout)
    except Exception as e:
        return f"❌ Failed to process booking. Error: {e}"

@tool
def block_calendar(input: str) -> str:
    """Creates a real Google Calendar event from the input like '9 AM'."""
    return real_block_calendar(input)
