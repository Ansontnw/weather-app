import streamlit as st
import requests
from datetime import datetime
import plotly.graph_objects as go

icon_url = "https://cdn2.iconfinder.com/data/icons/weather-flat-14/64/weather02-512.png"

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

def fetch_uv_index(api_key, lat, lon):
    url = f"http://api.openweathermap.org/data/2.5/uvi?appid={api_key}&lat={lat}&lon={lon}"
    response = requests.get(url)
    data = response.json()
    return data

def main():
    st.image(icon_url, width=100)
    st.title("Hello! Welcome to the Weather App")
    st.write("Enter the city name to get the weather data:")

    city = st.text_input("City")

    if st.button("Search"):
        if city:
            try:
                api_key = '4b379742cc1a830521251caf970d231e'
                weather_data = fetch_weather_data(api_key, city)
                forecast_data = fetch_forecast_data(api_key, city)

                if weather_data.get('cod') != 200:
                    st.write("Error:", weather_data.get('message', 'Failed to retrieve data'))
                else:
                    st.write(f"Weather in {weather_data['name']}, {weather_data['sys']['country']}:")
                    st.write(f"Temperature: {weather_data['main']['temp']}°C")
                    st.write(f"Description: {weather_data['weather'][0]['description'].capitalize()}")
                    st.write(f"Humidity: {weather_data['main']['humidity']}%")
                    st.write(f"Wind Speed: {weather_data['wind']['speed']} m/s")
                    
                    lat = weather_data['coord']['lat']
                    lon = weather_data['coord']['lon']
                    uv_data = fetch_uv_index(api_key, lat, lon)
                    if 'value' in uv_data:
                        st.write(f"UV Index: {uv_data['value']}")
                    else:
                        st.write("Failed to retrieve UV index data")

                    if forecast_data.get('cod') != "200":
                        st.write("Error:", forecast_data.get('message', 'Failed to retrieve forecast data'))
                    else:
                        st.header("5-Day Forecast:")
                        
                        dates = []
                        temps = []

                        for forecast in forecast_data['list']:
                            dt = datetime.fromtimestamp(forecast['dt'])
                            if dt.hour == 12:  # Show forecast for noon each day
                                dates.append(dt.strftime('%Y-%m-%d'))
                                temps.append(forecast['main']['temp'])
                                st.write(f"{dt.strftime('%Y-%m-%d %H:%M:%S')}:")
                                st.write(f"Temperature: {forecast['main']['temp']}°C")
                                st.write(f"Description: {forecast['weather'][0]['description'].capitalize()}")
                                st.write(f"Humidity: {forecast['main']['humidity']}%")
                                st.write(f"Wind Speed: {forecast['wind']['speed']} m/s")
                                st.write("---")
                        
                        # Plotting the temperature graph
                        fig = go.Figure(data=go.Scatter(x=dates, y=temps, mode='lines+markers'))
                        fig.update_layout(
                            title='5-Day Forecast Temperatures at Noon',
                            xaxis_title='Date',
                            yaxis_title='Temperature (°C)',
                            template='plotly_dark'
                        )
                        st.plotly_chart(fig)

            except Exception as e:
                st.write("Error fetching weather data:", e)
        else:
            st.write("Please enter a city name")

if __name__ == "__main__":
    main()
