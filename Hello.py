import streamlit as st
import requests
import pandas as pd
from datetime import datetime

image_url = "https://cdn2.iconfinder.com/data/icons/weather-flat-14/64/weather02-512.png"

#Define Wheather Data use Openweathermap API
def fetch_weather_data(api_key, city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    data = response.json()
    return data

#Define Forecast Data use Openweathermap API
def fetch_forecast_data(api_key, city):
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    data = response.json()
    return data

#Define UV Data use Openweathermap API
def fetch_uv_index(api_key, lat, lon):
    url = f"http://api.openweathermap.org/data/2.5/uvi?appid={api_key}&lat={lat}&lon={lon}"
    response = requests.get(url)
    data = response.json()
    return data

#Define Tide Data use Stromglass API
def fetch_tide_data(api_key, lat, lon):
    headers = {
        'Authorization': api_key
    }
    url = f"https://api.stormglass.io/v2/tide/extremes/point?lat={lat}&lng={lon}"
    response = requests.get(url, headers=headers)
    data = response.json()
    return data
    
def main():
    #Background Image
    background_image = """
        <style>
        [data-testid="stAppViewContainer"] > .main {
            background-image: url("https://unblast.com/wp-content/uploads/2018/06/Weather-Icons.jpg");
            background-size: 100vw 100vh;  # This sets the size to cover 100% of the viewport width and height
            background-position: center;
            background-repeat: no-repeat;
            opacity: 0.8;
        }
        </style>
        """
    #Print Background Image
    st.markdown(background_image, unsafe_allow_html=True)
    st.sidebar.image(image_url, width=100)
    st.sidebar.title("Hello! Welcome to the Weather App")
    st.sidebar.write("Enter the city name to get the weather data:")

    city = st.sidebar.text_input("Enter a City Name:")

    if st.sidebar.button("Search"):
        if city:
            try:
                weather_api_key = '4b379742cc1a830521251caf970d231e'
                stormglass_api_key = '5b92ecee-0b4e-11ef-a75c-0242ac130002-5b92ed66-0b4e-11ef-a75c-0242ac130002'
                weather_data = fetch_weather_data(weather_api_key, city)
                forecast_data = fetch_forecast_data(weather_api_key, city)

                # Check if the 'cod' field in the weather_data is not 200 (which means there was an error)
                if weather_data.get('cod') != 200:
                    st.write("Error:", weather_data.get('message', 'Failed to retrieve data'))
                else:
                    st.header("Current Weather Information")
                    st.write(f"Weather in {weather_data['name']}, {weather_data['sys']['country']}:")
                    st.write(f"Temperature: {weather_data['main']['temp']}°C")
                    st.write(f"Description: {weather_data['weather'][0]['description'].capitalize()}")
                    st.write(f"Humidity: {weather_data['main']['humidity']}%")
                    st.write(f"Wind Speed: {weather_data['wind']['speed']} m/s")

                    #Print Longitude and Latitude, UV Index
                    lat = weather_data['coord']['lat']
                    lon = weather_data['coord']['lon']
                    st.write(f"Latitude: {lat}")
                    st.write(f"Longitude: {lon}")
                    uv_data = fetch_uv_index(weather_api_key, lat, lon)
                    if 'value' in uv_data:
                        st.write(f"UV Index: {uv_data['value']}")
                    else:
                        st.write("Failed to retrieve UV index data")
                        
                    #Use Longitude and Latidue to get the tide information
                    tide_data = fetch_tide_data(stormglass_api_key, lat, lon)
                    if 'data' in tide_data:
                        st.header("Tide Information:")
                        
                        # Start with empty lists to store tide times and tide height
                        tide_times = []
                        tide_heights = []
                        
                        for tide in tide_data['data']:
                            tide_time = datetime.fromisoformat(tide['time'].replace('Z', '+00:00'))
                            tide_height = tide['height']
                            #st.write(f"Time: {tide_time.strftime('%Y-%m-%d %H:%M:%S')}, Height: {tide_height} meters")
                            tide_times.append(tide_time)
                            tide_heights.append(tide_height)
                        
                        # Time = Paksi X, Tide height = Paksi Y
                        tide_data_df = pd.DataFrame({'Time': tide_times, 'Tide Height': tide_heights})
                        st.line_chart(tide_data_df.set_index('Time'))
                    else:
                        st.write("Failed to retrieve tide data")
                        
                    # Check if the 'cod' field in the forcast_data is not 200 (which means there was an error)
                    if forecast_data.get('cod') != "200":
                        st.write("Error:", forecast_data.get('message', 'Failed to retrieve forecast data'))
                    else:
                        st.header("5-Day Forecast:")
                        
                        # Start with empty lists to store dates and temperatures
                        dates = []
                        temperatures = []
                        
                        for forecast in forecast_data['list']:
                            dt = datetime.fromtimestamp(forecast['dt'])
                            if dt.hour == 12:  # Show forecast for noon each day
                                st.write(f"{dt.strftime('%Y-%m-%d %H:%M:%S')}:")
                                st.write(f"Temperature: {forecast['main']['temp']}°C")
                                st.write(f"Description: {forecast['weather'][0]['description'].capitalize()}")
                                st.write(f"Humidity: {forecast['main']['humidity']}%")
                                st.write(f"Wind Speed: {forecast['wind']['speed']} m/s")
                                st.write("---")
                                dates.append(dt)
                                temperatures.append(forecast['main']['temp'])
                        
                        # Date = Paksi X, Temperature = Paksi Y        
                        data = pd.DataFrame({'Date':dates, 'Temperature':temperatures})
                        st.line_chart(data.set_index('Date'))

            except Exception as e:
                st.write("Error fetching weather data:", e)
        else:
            st.write("Please enter a city name")

if __name__ == "__main__":
    main()
