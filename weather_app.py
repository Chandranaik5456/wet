
import os
import streamlit as st
import requests
from datetime import datetime
import plotly.graph_objs as go

# Replace with your actual OpenWeatherMap API key
API_KEY = os.environ.get('https://api.openweathermap.org/data/2.5/weather?lat=44.34&lon=10.99&appid=bd5e378503939ddaee76f12ad7a97608', '')  # Fallback to empty string if not set

degree_sign = u'\N{DEGREE SIGN}'

st.title("Weather Information")
st.write("## Made by Jayvardhan Rathi with ❤️")

st.write("### Write the name of a City and select the Temperature Unit and Graph Type")

# Check if API key is provided
if not API_KEY:
    st.error("OpenWeatherMap API key is missing. Please set the OPENWEATHERMAP_API_KEY environment variable.")
    st.stop()

place = st.text_input("NAME OF THE CITY :", "")

if place == "":
    st.warning("Please input a city name!")

unit = st.selectbox("Select Temperature Unit", ("Celsius", "Fahrenheit"))
g_type = st.selectbox("Select Graph Type", ("Line Graph", "Bar Graph"))

unit_c = 'metric' if unit == 'Celsius' else 'imperial'

def get_weather_data(city):
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units={unit_c}'
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad responses
        return response.json()
    except requests.RequestException as e:
        st.error(f"Error fetching weather data: {e}")
        return None

def plot_temperatures_line(temp_min, temp_max):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=["Min Temp", "Max Temp"], y=[temp_min, temp_max], name='Temperatures'))
    fig.update_layout(title='Temperature Range')
    return fig

def plot_temperatures_bar(temp_min, temp_max):
    fig = go.Figure(
        data=[
            go.Bar(name='Minimum Temperature', x=["Min Temp"], y=[temp_min]),
            go.Bar(name='Maximum Temperature', x=["Max Temp"], y=[temp_max])
        ]
    )
    fig.update_layout(barmode='group', title='Temperature Range')
    return fig

def display_weather(city):
    data = get_weather_data(city)
    if not data or data.get("cod") != 200:
        st.error("City not found. Please check the name.")
        return

    # Extract weather data
    weather_info = data['weather'][0]
    main_info = data['main']
    wind_info = data['wind']
    cloud_info = data['clouds']
    sys_info = data['sys']

    temp_min = main_info['temp_min']
    temp_max = main_info['temp_max']
    humidity = main_info['humidity']
    pressure = main_info['pressure']
    wind_speed = wind_info['speed']
    cloud_coverage = cloud_info['all']
    
    sunrise_timestamp = sys_info['sunrise']
    sunset_timestamp = sys_info['sunset']
    
    # Convert timestamps to human-readable time
    timezone_offset = data['timezone']
    sunrise_time = datetime.utcfromtimestamp(sunrise_timestamp + timezone_offset)
    sunset_time = datetime.utcfromtimestamp(sunset_timestamp + timezone_offset)

    # Display basic weather information
    st.write(f"### Weather in {city}: {weather_info['main']} - {weather_info['description']}")
    st.write(f"Temperature: {temp_min}{degree_sign} - {temp_max}{degree_sign}")
    st.write(f"Humidity: {humidity}%")
    st.write(f"Pressure: {pressure} hPa")
    st.write(f"Wind Speed: {wind_speed} m/s")
    st.write(f"Cloud Coverage: {cloud_coverage}%")

    # Display sunrise and sunset times
    st.write(f"Sunrise Time: {sunrise_time.strftime('%H:%M:%S')}")
    st.write(f"Sunset Time: {sunset_time.strftime('%H:%M:%S')}")

    # Plot the temperature data
    if g_type == "Line Graph":
        fig = plot_temperatures_line(temp_min, temp_max)
        st.plotly_chart(fig)
    elif g_type == "Bar Graph":
        fig = plot_temperatures_bar(temp_min, temp_max)
        st.plotly_chart(fig)

def updates(city):
    data = get_weather_data(city)
    if data and 'weather' in data:
        st.title("Impending Weather Alerts:")
        # Check for specific weather conditions
        for weather in data['weather']:
            if weather['main'].lower() in ['rain', 'storm', 'snow', 'thunderstorm']:
                st.write(f"### {weather['main']} Alert!")

# Main execution
if st.button("Get Weather") and place:
    display_weather(place)
    updates(place)
