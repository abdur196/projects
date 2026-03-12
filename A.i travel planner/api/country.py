# country.py
import requests

GAPI_KEY = "d28971fe983d4f09aa6feb4f84045210"

def get_country_from_city(city_name: str) -> str | None:
   
    try:
        url = f"https://api.geoapify.com/v1/geocode/search?text={city_name}&apiKey={GAPI_KEY}"
        resp = requests.get(url)
        resp.raise_for_status()
        data = resp.json()
        
        features = data.get("features")
        if not features:
            return None
        
        return features[0]["properties"].get("country")
    except requests.RequestException as e:
        print("Error fetching country:", e)
        return None


def get_country_info(country_name: str) -> dict | None:
    """
    Fetch general country info (currency, language, timezone, population, flag) 
    from REST Countries API.
    """
    try:
        url = f"https://restcountries.com/v3.1/name/{country_name}"
        resp = requests.get(url)
        resp.raise_for_status()
        data = resp.json()
        if not data:
            return None
        
        country = data[0]
        return {
            "name": country.get("name", {}).get("common"),
            "official_name": country.get("name", {}).get("official"),
            "capital": country.get("capital", [None])[0],
            "region": country.get("region"),
            "subregion": country.get("subregion"),
            "languages": list(country.get("languages", {}).values()),
            "currencies": list(country.get("currencies", {}).keys()),
            "timezones": country.get("timezones", []),
            "population": country.get("population"),
            "flag": country.get("flags", {}).get("png"),
        }
    except requests.RequestException as e:
        print("Error fetching country info:", e)
        return None


# Example usage
if __name__ == "__main__":
    city = "Paris"
    country = get_country_from_city(city)
    if country:
        info = get_country_info(country)
        print(f"City: {city}")
        print(f"Country: {country}")
        print("Country Info:", info)
    else:
        print("Could not resolve city to country.")
