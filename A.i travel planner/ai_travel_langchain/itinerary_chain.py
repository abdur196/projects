from langchain.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI

from datetime import datetime, timedelta
from api.country import get_country_from_city, get_country_info
from api.places import get_lat_lon, get_places_nearby
from api.weather import get_weather_forecast
from api.tips import get_travel_tips


def flatten_weather(data):
    daily = data["daily"]
    days = []

    for date, t_max, t_min, h_max, h_min, code in zip(
        daily["time"],
        daily["temperature_2m_max"],
        daily["temperature_2m_min"],
        daily["relative_humidity_2m_max"],
        daily["relative_humidity_2m_min"],
        daily["weathercode"],
    ):
        day = {
            "date": date,
            "temperature_max": float(t_max),
            "temperature_min": float(t_min),
            "humidity_max": int(h_max),
            "humidity_min": int(h_min),
            "weather_code": int(code),
        }
        days.append(day)

    return days





def generate_itinerary(city, duration=3, start_date=None):
    
    country_name = get_country_from_city(city)
    country_info = get_country_info(country_name)

    
    lat, lon = get_lat_lon(city)

    
    if start_date:
        start = datetime.strptime(start_date, "%Y-%m-%d")
    else:
        start = datetime.today()
    end = start + timedelta(days=duration - 1)

   
    weather_data = get_weather_forecast(lat, lon, duration, start.strftime("%Y-%m-%d"))

  
    flattened = flatten_weather(weather_data)

    
    places = get_places_nearby(lat, lon)
    travel_tips = get_travel_tips(city)

    
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        google_api_key="AIzaSyAR445iW0Y0PYKU9tWbVGUfpkLwGLCcpOo",
        temperature=0.7,
    )

    prompt = PromptTemplate(
        input_variables=["city", "country_info", "weather_data", "places", "travel_tips", "duration"],
        template="""
You are a travel planner. Create a {duration}-day itinerary for {city}.

Country details: {country_info}
Weather forecast: {weather_data}
Nearby attractions/restaurants: {places}
Travel tips: {travel_tips}

Format the output clearly with:
- Morning, Afternoon, Evening activities and a weather note for each day.
- Weather notes must use exact values from weather_data (temperature, humidity).
- Local tips at the end of the day.
- Translate weather codes into human-readable format.

Structure the output like this:

**Day 1 (Sunny, 29°C)**
- Weather note:
- Morning:
- Afternoon:
- Evening:
- Tip: *

**Day 2**
- Weather note:
- Morning:
- Afternoon:
- Evening:
- Tip: *

**Day 3**
- Weather note:
- Morning:
- Afternoon:
- Evening:
- Tip: *
 

"""
    )

    chain = prompt | llm
    result = chain.invoke({
        "city": city,
        "country_info": country_info,
        "weather_data": flattened,
        "places": places,
        "travel_tips": travel_tips,
        "duration": duration
    })

    return result.content  


def main():
   
    city = "paris"
    duration = 3
    start_date = "2025-08-25"
    itinerary = generate_itinerary(city, duration, start_date)
    print("\n\n=== Your Best Vacation ===\n")
    print(itinerary)


if __name__ == "__main__":
    main()
