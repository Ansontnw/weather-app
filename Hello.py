import streamlit as st
import requests
import matplotlib.pyplot as plt
import pandas as pd

def fetch_weather_data(api_key, city):
    url = f"http://api.weatherstack.com/current?access_key={api_key}&query={city}"
    response = requests.get(url)
    data = response.json()
    return data

def fetch_forecast_data(api_key, city):
    url = f"http://api.weatherstack.com/forecast?access_key={api_key}&query={city}&forecast_days=3"
    response = requests.get(url)
    data = response.json()
    return data

def fetch_tide_data(api_key, lat, lng):
    url = f"https://api.stormglass.io/v2/tide/extremes/point?lat={lat}&lng={lng}&start=now&end=24"
    headers = {'Authorization': api_key}
    response = requests.get(url, headers=headers)
    data = response.json()
    return data

def plot_tide_chart(tide_data):
    times = [entry['time'] for entry in tide_data['data']]
    heights = [entry['height'] for entry in tide_data['data']]
    
    plt.figure(figsize=(10, 6))
    plt.plot(times, heights, marker='o', linestyle='-')
    plt.xlabel('Time')
    plt.ylabel('Tide Height (meters)')
    plt.title('Tide Height Over Time')
    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot()

def main():
    st.title("Weather, Tide, and Forecast App")
    st.write("Enter the city name to get the current weather, tide information, and 3-day forecast:")

    city = st.text_input("City")

    if st.button("Get Weather, Tide & Forecast"):
        if city:
            try:
                weather_data = fetch_weather_data(api_key='0f33509df08b7bea7f411f2e27c75430', city=city)

                if 'error' in weather_data:
                    st.write("Error:", weather_data['error']['info'])
                else:
                    st.write(f"Weather in {city}:")
                    st.write(f"Temperature: {weather_data['current']['temperature']}°C")
                    st.write(f"Humidity: {weather_data['current']['humidity']}%")
                    st.write(f"Wind Speed: {weather_data['current']['wind_speed']} m/s")

                forecast_data = fetch_forecast_data(api_key='0f33509df08b7bea7f411f2e27c75430', city=city)
                if 'error' in forecast_data:
                    st.write("Error fetching forecast:", forecast_data['error']['info'])
                else:
                    st.write("3-Day Forecast:")
                    for day in forecast_data['forecast']['forecastday']:
                        date = day['date']
                        max_temp = day['day']['maxtemp_c']
                        min_temp = day['day']['mintemp_c']
                        condition = day['day']['condition']['text']
                        st.write(f"Date: {date}, Max Temp: {max_temp}°C, Min Temp: {min_temp}°C, Condition: {condition}")

                if 'location' in weather_data:
                    lat = weather_data['location']['lat']
                    lng = weather_data['location']['lon']
                    tide_data = fetch_tide_data(api_key='5b92ecee-0b4e-11ef-a75c-0242ac130002-5b92ed66-0b4e-11ef-a75c-0242ac130002', lat=lat, lng=lng)
                    if 'data' in tide_data:
                        st.write("Tide Information:")
                        for entry in tide_data['data']:
                            st.write(f"Time: {entry['time']}, Height: {entry['height']} meters")
                        plot_tide_chart(tide_data)
                    else:
                        st.write("No tide data available")
                
            except Exception as e:
                st.write("Error fetching data:", e)
        else:
            st.write("Please enter a city name")

if __name__ == "__main__":
    main()
