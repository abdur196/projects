import requests

def get_travel_tips(place: str, language: str = "en") -> str:
    """
    Fetch travel tips or information about a place from Wikivoyage using MediaWiki API.
    
    Args:
        place (str): Name of the city or country.
        language (str): Language code (default = "en" for English).
    
    Returns:
        str: Extracted travel tips or summary.
    """
    url = f"https://{language}.wikivoyage.org/w/api.php"
    params = {
        "action": "query",
        "prop": "extracts",
        "exintro": True,
        "explaintext": True,
        "titles": place,
        "format": "json",
    }
    headers = {
        "User-Agent": "MyTravelApp/1.0 (contact: your_email@example.com)"  
        # <-- important so they don't block you
    }

    try:
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()
        data = response.json()

        pages = data.get("query", {}).get("pages", {})
        for _, page in pages.items():
            if "extract" in page:
                return page["extract"]

        return f"No travel tips found for {place}."

    except Exception as e:
        return f"Error fetching tips: {str(e)}"


# Test usage
if __name__ == "__main__":
    city = "osaka"
    tips = get_travel_tips(city)
    print(f"Travel Tips for {city}:\n{tips}")
