import streamlit as st
import requests

def fetch_weather_data(api_key, city):
    url = f"http://api.weatherstack.com/current?access_key={api_key}&query={city}"
    response = requests.get(url)
    data = response.json()
    return data

def fetch_location_data(api_key, latitude, longitude):
    url = f"http://api.weatherstack.com/current?access_key={api_key}&query={latitude},{longitude}"
    response = requests.get(url)
    data = response.json()
    return data

def main():
    st.title("Hello!, Welcome to Weather App")
    st.write("Enter the city name to get the current weather:")

    city = st.text_input("City")

    if st.button("Search"):
        if city:
            try:
                weather_data = fetch_weather_data(api_key='0f33509df08b7bea7f411f2e27c75430', city=city)

                if 'error' in weather_data:
                    st.write("Error:", weather_data['error']['info'])
                else:
                    st.write(f"Weather in {weather_data['location']['name']}, {weather_data['location']['region']}, {weather_data['location']['country']}:")
                    st.write(f"Temperature: {weather_data['current']['temperature']}°C")
                    st.write(f"Description: {weather_data['current']['weather_descriptions'][0]}")
                    st.write(f"Humidity: {weather_data['current']['humidity']}%")
                    st.write(f"Wind Speed: {weather_data['current']['wind_speed']} m/s")

            except Exception as e:
                st.write("Error fetching weather data:", e)
        else:
            st.write("Please enter a city name")

if __name__ == "__main__":
    main()
