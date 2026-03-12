# places.py
import requests

GEO_API_KEY = "d28971fe983d4f09aa6feb4f84045210"
GAPI_KEY = "a77db3cc5a1ed05fa37db83688bc1b36"


def get_lat_lon(city_name):
    """
    Returns latitude and longitude for a given city using OpenWeatherMap Geocoding API.
    """
    url = f"http://api.openweathermap.org/geo/1.0/direct?q={city_name}&limit=1&appid={GAPI_KEY}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        if data:
            return data[0]["lat"], data[0]["lon"]
        else:
            raise ValueError(f"City '{city_name}' not found.")
    else:
        raise ConnectionError(f"Error {response.status_code} while fetching city coordinates.")


def get_places_nearby(  lat, lon,radius=5000, limit=50):
    """
    Returns nearby places for a given city using Geoapify Places API.

    :param city_name: str, city name
    :param radius: int, search radius in meters
    :param limit: int, max number of places to return
    :return: list of dicts containing place info
    """
    

    categories = [
        "entertainment.museum",
        "catering.restaurant",
        "catering.fast_food",
        "catering.cafe",
        "catering.pub",
        "catering.bar",
        "accommodation.hotel",
        "accommodation.motel",
        "entertainment.culture.theatre",
        "entertainment.culture.arts_centre",
        "entertainment.culture.gallery",
        "entertainment.theme_park",
        "entertainment.water_park",
        "leisure.picnic",
        "natural.water",
        "natural.mountain.peak",
        "natural.mountain.glacier",
        "natural.mountain.cliff",
        "tourism.attraction",
        "tourism.attraction.viewpoint"
    ]

    categories_str = ",".join(categories)

    url = (
        f"https://api.geoapify.com/v2/places?"
        f"categories={categories_str}&filter=circle:{lon},{lat},{radius}&limit={limit}&apiKey={GEO_API_KEY}"
    )

    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        features = data.get("features", [])
        places = []
        for place in features:
            props = place.get("properties", {})
            places.append({
                "name": props.get("name"),
                "categories": props.get("categories"),
                "address": props.get("address_line1")
            })
        return places
    else:
        raise ConnectionError(f"Error {response.status_code}: {response.text}")


# Example usage
if __name__ == "__main__":
    city = "Paris"
    nearby_places = get_places_nearby(city)
    print(f"Nearby places in {city}:")
    for place in nearby_places:
        print(place["name"], "-", place["categories"], "-", place["address"])
