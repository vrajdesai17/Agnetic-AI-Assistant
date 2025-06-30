import os
import requests
from dotenv import load_dotenv

load_dotenv()
client_id = os.getenv("AMADEUS_CLIENT_ID")
client_secret = os.getenv("AMADEUS_CLIENT_SECRET")

def get_access_token():
    url = "https://test.api.amadeus.com/v1/security/oauth2/token"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret
    }
    response = requests.post(url, headers=headers, data=data)
    if response.status_code == 200:
        return response.json()["access_token"]
    return None

def search_flights(origin, destination, departure_date):
    token = get_access_token()
    if not token:
        return "❌ Could not get access token."
    url = "https://test.api.amadeus.com/v2/shopping/flight-offers"
    headers = { "Authorization": f"Bearer {token}" }
    params = {
        "originLocationCode": origin,
        "destinationLocationCode": destination,
        "departureDate": departure_date,
        "adults": 1,
        "max": 3
    }
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        data = response.json().get("data", [])
        if not data:
            return "⚠️ No flights found."
        output = []
        for i, offer in enumerate(data):
            segments = offer["itineraries"][0]["segments"]
            segment_info = [f"{seg['departure']['iataCode']} ➜ {seg['arrival']['iataCode']} at {seg['departure']['at']}" for seg in segments]
            output.append(f"✈️ Offer #{i + 1}:\n" + "\n".join(segment_info))
        return "\n\n".join(output)
    return f"❌ API Error!\nStatus: {response.status_code}\nDetails: {response.text}"
