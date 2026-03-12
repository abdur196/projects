# weather.py
import requests
from datetime import datetime, timedelta

API_KEY = "a77db3cc5a1ed05fa37db83688bc1b36"


def get_lat_lon(city_name):
   
    url = f"http://api.openweathermap.org/geo/1.0/direct?q={city_name}&limit=1&appid={API_KEY}"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        if data:  # if we got results
            lat = data[0]["lat"]
            lon = data[0]["lon"]
            return lat, lon
        else:
            raise ValueError(f"City '{city_name}' not found.")
    else:
        raise ConnectionError(f"Error {response.status_code} while fetching city coordinates.")


def get_weather_forecast( lat, lon, duration_days=3, start_date=None):
   
    

    if start_date:
        start = datetime.strptime(start_date, "%Y-%m-%d")
    else:
        start = datetime.utcnow()

    end = start + timedelta(days=duration_days - 1)

    start_str = start.strftime("%Y-%m-%d")
    end_str = end.strftime("%Y-%m-%d")

    url = (
        f"https://api.open-meteo.com/v1/forecast?"
        f"latitude={lat}&longitude={lon}"
        f"&start_date={start_str}&end_date={end_str}"
        f"&daily=temperature_2m_max,temperature_2m_min,relative_humidity_2m_max,"
        f"relative_humidity_2m_min,weathercode"
        f"&timezone=auto"
    )

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        return data
    else:
        raise ConnectionError(f"Error {response.status_code}: {response.text}")


# Example usage
if __name__ == "__main__":
    city = "Paris"
    start_date = "2025-08-30"
    forecast = get_weather_forecast(64,100, duration_days=3, start_date=start_date)
    print(f"Weather forecast for {city}:")
    print(forecast)
