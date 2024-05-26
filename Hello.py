import streamlit as st
import requests
from datetime import datetime

def fetch_weather_data(api_key, city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    data = response.json()
    return data

def fetch_forecast_data(api_key, city):
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    data = response.json()
    return data

def main():
    st.title("Hello!, Welcome to Weather App")
    st.write("Enter the city name to get the weather data:")

    city = st.text_input("City")

    if st.button("Search"):
        if city:
            try:
                weather_data = fetch_weather_data(api_key='4b379742cc1a830521251caf970d231e', city=city)
                forecast_data = fetch_forecast_data(api_key='4b379742cc1a830521251caf970d231e', city=city)

                if weather_data.get('cod') != 200:
                    st.write("Error:", weather_data.get('message', 'Failed to retrieve data'))
                else:
                    st.write(f"Weather in {weather_data['name']}, {weather_data['sys']['country']}:")
                    st.write(f"Temperature: {weather_data['main']['temp']}°C")
                    st.write(f"Description: {weather_data['weather'][0]['description'].capitalize()}")
                    st.write(f"Humidity: {weather_data['main']['humidity']}%")
                    st.write(f"Wind Speed: {weather_data['wind']['speed']} m/s")

                    if forecast_data.get('cod') != "200":
                        st.write("Error:", forecast_data.get('message', 'Failed to retrieve forecast data'))
                    else:
                        st.write("5-Day Forecast:")
                        for forecast in forecast_data['list']:
                            dt = datetime.fromtimestamp(forecast['dt'])
                            if dt.hour == 12:  # Show forecast for noon each day
                                st.write(f"{dt.strftime('%Y-%m-%d %H:%M:%S')}:")
                                st.write(f"Temperature: {forecast['main']['temp']}°C")
                                st.write(f"Description: {forecast['weather'][0]['description'].capitalize()}")
                                st.write(f"Humidity: {forecast['main']['humidity']}%")
                                st.write(f"Wind Speed: {forecast['wind']['speed']} m/s")
                                st.write("---")

            except Exception as e:
                st.write("Error fetching weather data:", e)
        else:
            st.write("Please enter a city name")

if __name__ == "__main__":
    main()
