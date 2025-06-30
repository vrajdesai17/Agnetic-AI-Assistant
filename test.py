import requests

url = "https://hotels4.p.rapidapi.com/locations/v3/search"

querystring = {
    "q": "Paris",
    "locale": "en_US",
    "langid": "1033",
    "siteid": "300000001"
}

headers = {
    "X-RapidAPI-Key": "8e59401748mshf6028adabdd809dp1d1ce8jsnab01012bcb45",
    "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
}

response = requests.get(url, headers=headers, params=querystring)
print(response.json())
