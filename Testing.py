import requests

API_KEY = "PASTE_YOUR_KEY_HERE"

url = "https://api.openweathermap.org/data/2.5/weather"

params = {
    "q": "Delhi",
    "appid": "44df019b5cb3ffe4241fce1bfbabacc2",
    "units": "metric"
}

response = requests.get(url, params=params)

print(response.json())