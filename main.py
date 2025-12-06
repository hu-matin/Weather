from src.Weather import Weather
from src.Card import WeatherCardApp

API = open('config/api.txt', 'r').read().strip()

weather = Weather(API)

app = WeatherCardApp(weather)
app.mainloop()


