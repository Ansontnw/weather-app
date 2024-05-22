import streamlit as st
import requests
#import matplotlib.pyplot as plt
from datetime import datetime

# Function to fetch current weather data from OpenWeatherMap
def fetch_weather_data(api_key, city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    data = response.json()
    return data

# Function to fetch 3-day forecast data from OpenWeatherMap
def fetch_forecast_data(api_key, city):
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    data = response.json()
    return data

# Function to fetch tide data from StormGlass
def fetch_tide_data(api_key, lat, lng):
    url = f"https://api.stormglass.io/v2/tide/extremes/point?lat={lat}&lng={lng}&start=now&end=now+3d"
    headers = {'Authorization': api_key}
    response = requests.get(url, headers=headers)
    data = response.json()
    return data

# Function to plot tide data
def plot_tide_chart(tide_data):
    times = [datetime.strptime(entry['time'], '%Y-%m-%dT%H:%M:%S%z') for entry in tide_data['data']]
    heights = [entry['height'] for entry in tide_data['data']]
    
    plt.figure(figsize=(10, 6))
    plt.plot(times, heights, marker='o', linestyle='-')
    plt.xlabel('Time')
    plt.ylabel('Tide Height (meters)')
    plt.title('Tide Height Over Time')
    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot(plt)

def main():
    st.title("Weather, Tide, and Forecast App")
    st.write("Enter the city name to get the current weather, tide information, and 3-day forecast:")

    city = st.text_input("City")

    if st.button("Get Weather, Tide & Forecast"):
        if city:
            try:
                weather_api_key = '4b379742cc1a830521251caf970d231e'
                tide_api_key = '5b92ecee-0b4e-11ef-a75c-0242ac130002-5b92ed66-0b4e-11ef-a75c-0242ac130002'
                
                # Fetch current weather data
                weather_data = fetch_weather_data(api_key=weather_api_key, city=city)
                if weather_data.get('cod') != 200:
                    st.write("Error:", weather_data.get('message', 'Unable to fetch weather data'))
                else:
                    st.write(f"Weather in {city}:")
                    st.write(f"Temperature: {weather_data['main']['temp']}°C")
                    st.write(f"Description: {weather_data['weather'][0]['description'].capitalize()}")
                    st.write(f"Humidity: {weather_data['main']['humidity']}%")
                    st.write(f"Wind Speed: {weather_data['wind']['speed']} m/s")
                
                # Fetch 3-day forecast data
                forecast_data = fetch_forecast_data(api_key=weather_api_key, city=city)
                if forecast_data.get('cod') != '200':
                    st.write("Error fetching forecast:", forecast_data.get('message', 'Unable to fetch forecast data'))
                else:
                    st.write("3-Day Forecast:")
                    forecast_list = forecast_data['list']
                    for i in range(0, 24*3, 8):  # 3 days, 8 three-hour intervals per day
                        forecast = forecast_list[i]
                        date = datetime.fromtimestamp(forecast['dt']).strftime('%Y-%m-%d %H:%M:%S')
                        temp = forecast['main']['temp']
                        description = forecast['weather'][0]['description'].capitalize()
                        st.write(f"Date: {date}, Temp: {temp}°C, Condition: {description}")

                # Fetch and plot tide data
                if 'coord' in weather_data:
                    lat = weather_data['coord']['lat']
                    lng = weather_data['coord']['lon']
                    tide_data = fetch_tide_data(api_key=tide_api_key, lat=lat, lng=lng)
                    if 'data' in tide_data:
                        st.write("Tide Information:")
                        for entry in tide_data['data']:
                            time = datetime.strptime(entry['time'], '%Y-%m-%dT%H:%M:%S%z').strftime('%Y-%m-%d %H:%M:%S')
                            st.write(f"Time: {time}, Height: {entry['height']} meters")
                        plot_tide_chart(tide_data)
                    else:
                        st.write("No tide data available")
                
            except Exception as e:
                st.write("Error fetching data:", e)
        else:
            st.write("Please enter a city name")

if __name__ == "__main__":
    main()
