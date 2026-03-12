import streamlit as st
from datetime import date, timedelta
from ai_travel_langchain.itinerary_chain import generate_itinerary

st.set_page_config(page_title="🌍 AI Travel Planner", layout="wide")

st.title("🌍 Smart AI Travel Planner")
st.write("Plan your trip with AI-powered personalized itineraries.")


today = date.today()
max_forecast_date = today + timedelta(days=15)  # 16 days including today


city = st.text_input("Enter your destination:")
duration = st.number_input(
    "Number of days:",
    min_value=3,
    max_value=3,
    value=3,
    step=1
)

start_date = st.date_input("Start Date:", min_value=today, max_value=max_forecast_date)


if st.button("✨ Generate Itinerary"):
    with st.spinner("Planning your dream trip..."):
        # Check if trip end date exceeds forecast range
        trip_end_date = start_date + timedelta(days=duration - 1)

        if start_date < today:
            st.error("⚠️ Start date cannot be in the past.")
        elif start_date > max_forecast_date:
            st.error("⚠️ Start date must be within the next 16 days.")
        elif trip_end_date > max_forecast_date:
            st.error(
                f"⚠️ Your trip of {duration} days exceeds the forecast window.\n"
                f"Latest possible end date is {max_forecast_date}."
            )
        else:
            try:
                itinerary = generate_itinerary(city, duration, str(start_date))
                st.success("Here’s your personalized itinerary:")
                st.markdown(itinerary)
            except Exception as e:
                st.error(f"⚠️ Error: {e}")
