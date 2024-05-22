import streamlit as st
import requests

def fetch_weather_data(api_key, city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    data = response.json()
    return data

def fetch_location_data(api_key, latitude, longitude):
    url = f"http://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&appid={api_key}&units=metric"
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
                weather_data = fetch_weather_data(api_key='4b379742cc1a830521251caf970d231e', city=city)

                if weather_data.get('cod') != 200:
                    st.write("Error:", weather_data.get('message', 'Failed to retrieve data'))
                else:
                    st.write(f"Weather in {weather_data['name']}, {weather_data['sys']['country']}:")
                    st.write(f"Temperature: {weather_data['main']['temp']}°C")
                    st.write(f"Description: {weather_data['weather'][0]['description'].capitalize()}")
                    st.write(f"Humidity: {weather_data['main']['humidity']}%")
                    st.write(f"Wind Speed: {weather_data['wind']['speed']} m/s")

            except Exception as e:
                st.write("Error fetching weather data:", e)
        else:
            st.write("Please enter a city name")

if __name__ == "__main__":
    main()
