import requests

RAPID_API_KEY = "YOURKEY"  
HEADERS = {
    "X-RapidAPI-Key": RAPID_API_KEY,
    "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
}

def get_location_id(city):
    url = "https://hotels4.p.rapidapi.com/locations/v3/search"
    params = {"q": city, "locale": "en_US", "langid": "1033", "siteid": "300000001"}
    response = requests.get(url, headers=HEADERS, params=params)
    data = response.json()
    return data['sr'][0]['gaiaId'] if data.get("sr") else None

def get_hotels_in_city(city, checkin, checkout):
    region_id = get_location_id(city)
    if not region_id:
        return f"❌ Could not find region ID for city '{city}'"

    url = "https://hotels4.p.rapidapi.com/properties/v2/list"
    payload = {
        "currency": "USD",
        "eapid": 1,
        "locale": "en_US",
        "siteId": 300000001,
        "destination": {"regionId": region_id},
        "checkInDate": dict(zip(["day", "month", "year"], map(int, checkin.split("-")[2::-1]))),
        "checkOutDate": dict(zip(["day", "month", "year"], map(int, checkout.split("-")[2::-1]))),
        "rooms": [{"adults": 1}],
        "resultsStartingIndex": 0,
        "resultsSize": 3,
        "sort": "PRICE_LOW_TO_HIGH"
    }
    response = requests.post(url, headers=HEADERS, json=payload)
    if response.status_code != 200:
        return f"❌ API error: {response.status_code}, {response.text}"
    
    hotels = response.json()['data']['propertySearch']['properties']
    if not hotels:
        return f"⚠️ No hotels found in {city}."

    out = []
    for idx, h in enumerate(hotels, start=1):
        name = h['name']
        price = h['price']['lead']['formatted']
        out.append(f"🏨 Option #{idx}: {name} — {price}")
    return "\n\n".join(out)
