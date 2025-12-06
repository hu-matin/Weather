import requests
from pprint import pprint


class Weather:
    BASE_URL = 'https://api.openweathermap.org/data/2.5/forecast?'

    def __init__(self, api_key: str, city: str = 'London'):
        self.api_key = api_key
        self.city = city
        self.data = None

    def get(self):
        try:
            url = self.BASE_URL + f'q={self.city}&appid={self.api_key}'
            response = requests.get(url, timeout=20)
            response.raise_for_status()
            data = response.json()

            item = data['list'][0]
            self.data = {
                "city": data['city']['name'],
                "country": data['city']['country'],
                "temp": round(item['main']['temp'] - 273.15, 1),
                "feels_like": round(item['main']['feels_like'] - 273.15, 1),
                "temp_min": round(item['main']['temp_min'] - 273.15, 1),
                "temp_max": round(item['main']['temp_max'] - 273.15, 1),
                "humidity": item['main']['humidity'],
                "pressure": item['main']['pressure'],
                "description": item['weather'][0]['description'],
                "icon": item['weather'][0]['icon'],
                "main": item['weather'][0]['main'],
                "wind_speed": item['wind']['speed'],
            }
            return self.data
        except requests.HTTPError as e:
            print(f"HTTP Error: {e}")
            return None
        except requests.RequestException as e:
            print(f"Network error: {e}")
            return None
        except KeyError as e:
            print(f"API response error: {e}")
            return None

    def print_all(self, mode: str = 'all') -> None:
        if not self.data:
            print("Please first run get() method.")
            return

        if mode not in ['all', 'li']:
            print("Valid modes: 'all' or 'li'")
            return

        match mode:
            case "li":
                li = [f"{k}: {v}" for k, v in self.data.items()]
                pprint(li)
            case "all":
                for k, v in self.data.items():
                    print(f"{k}: {v}")
            case _:
                print("Valid modes: 'all' or 'li'")
