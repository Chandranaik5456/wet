import os
import pytz
import pyowm
import streamlit as st
from matplotlib import dates
from datetime import datetime
from matplotlib import pyplot as plt
import plotly.graph_objects as go
import plotly.express as px


API_KEY = os.environ.get('https://api.openweathermap.org/data/2.5/weather?lat=44.34&lon=10.99&appid=bd5e378503939ddaee76f12ad7a97608')
owm = pyowm.OWM(API_KEY)
mgr=owm.weather_manager()

degree_sign= u'\N{DEGREE SIGN}'

st.title("5 Day Weather Forecast")
st.write("## Made by Jayvardhan Rathi with ❤️")

st.write("### Write the name of a City and select the Temperature Unit and Graph Type from the sidebar")

place=st.text_input("NAME OF THE CITY :", "")


if place == None:
    st.write("Input a CITY!")



unit=st.selectbox("Select Temperature Unit",("Celsius","Fahrenheit"))

g_type=st.selectbox("Select Graph Type",("Line Graph","Bar Graph"))

if unit == 'Celsius':
    unit_c = 'celsius'
else:
    unit_c = 'fahrenheit'


def get_temperature():
    days = []
    dates = []
    temp_min = []
    temp_max = []
    forecaster = mgr.forecast_at_place(place, '3h')
    forecast=forecaster.forecast
    for weather in forecast:
        day=datetime.utcfromtimestamp(weather.reference_time())
        #day = gmt_to_eastern(weather.reference_time())
        date = day.date()
        if date not in dates:
            dates.append(date)
            temp_min.append(None)
            temp_max.append(None)
            days.append(date)
        temperature = weather.temperature(unit_c)['temp']
        if not temp_min[-1] or temperature < temp_min[-1]:
            temp_min[-1] = temperature
        if not temp_max[-1] or temperature > temp_max[-1]:
            temp_max[-1] = temperature
    return(days, temp_min, temp_max)

def init_plot():
     plt.figure('PyOWM Weather', figsize=(5,4))
     plt.xlabel('Day')
     plt.ylabel(f'Temperature ({degree_sign}F)')
     plt.title('Weekly Forecast')



def plot_temperatures(days, temp_min, temp_max):
    # days = dates.date2num(days)
    fig = go.Figure(
        data=[
            go.Bar(name='minimum temperatures', x=days, y=temp_min),
            go.Bar(name='maximum temperatures', x=days, y=temp_max)
        ]
    )
    fig.update_layout(barmode='group')
    return fig


def plot_temperatures_line(days, temp_min, temp_max):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=days, y=temp_min, name='minimum temperatures'))
    fig.add_trace(go.Scatter(x=days, y=temp_max, name='maximimum temperatures'))
    return fig

def label_xaxis(days):
    plt.xticks(days)
    axes = plt.gca()
    xaxis_format = dates.DateFormatter('%m/%d')
    axes.xaxis.set_major_formatter(xaxis_format)

def draw_bar_chart():
    days, temp_min, temp_max = get_temperature()
    fig = plot_temperatures(days, temp_min, temp_max)
    # write_temperatures_on_bar_chart(bar_min, bar_max)
    st.plotly_chart(fig)
    st.title("Minimum and Maximum Temperatures")
    for i in range (0,5):
        st.write("### ",temp_min[i],degree_sign,' --- ',temp_max[i],degree_sign)


def draw_line_chart():
    days, temp_min, temp_max = get_temperature()
    fig = plot_temperatures_line(days, temp_min, temp_max)
    st.plotly_chart(fig)
    st.title("Minimum and Maximum Temperatures")
    for i in range (0,5):
        st.write("### ",temp_min[i],degree_sign,' --- ',temp_max[i],degree_sign)

def other_weather_updates():
    forecaster = mgr.forecast_at_place(place, '3h')
    st.title("Impending Temperature Changes :")
    if forecaster.will_have_fog():
        st.write("### FOG Alert!")
    if forecaster.will_have_rain():
        st.write("### Rain Alert")
    if forecaster.will_have_storm():
        st.write("### Storm Alert!")
    if forecaster.will_have_snow():
        st.write("### Snow Alert!")
    if forecaster.will_have_tornado():
        st.write("### Tornado Alert!")
    if forecaster.will_have_hurricane():
        st.write("### Hurricane Alert!")
    if forecaster.will_have_clouds():
        st.write("### Cloudy Skies")    
    if forecaster.will_have_clear():
        st.write("### Clear Weather!")

def cloud_and_wind():
    obs=mgr.weather_at_place(place)
    weather=obs.weather
    cloud_cov=weather.clouds
    winds=weather.wind()['speed']
    st.title("Cloud coverage and wind speed")
    st.write('### The current cloud coverage for',place,'is',cloud_cov,'%')
    st.write('### The current wind speed for',place, 'is',winds,'mph')

def sunrise_and_sunset():
    obs=mgr.weather_at_place(place)
    weather=obs.weather
    st.title("Sunrise and Sunset Times :")
    india = pytz.timezone("Asia/Kolkata")
    ss=weather.sunset_time(timeformat='iso')
    sr=weather.sunrise_time(timeformat='iso')  
    st.write("### Sunrise time in",place,"is",sr)
    st.write("### Sunset time in",place,"is",ss)

def updates():
    other_weather_updates()
    cloud_and_wind()
    sunrise_and_sunset()


if __name__ == '__main__':
    
    if st.button("SUBMIT"):
        if g_type == 'Line Graph':
            draw_line_chart()    
        else:
            draw_bar_chart()
        updates()
API_KEY = os.environ.get('OPENWEATHERMAP_API_KEY') 

degree_sign = u'\N{DEGREE SIGN}'

st.title("Weather Information")
st.write("## Made by Jayvardhan Rathi with ❤️")

st.write("### Write the name of a City and select the Temperature Unit and Graph Type from the sidebar")

place = st.text_input("NAME OF THE CITY :", "")

if place == "":
    st.warning("Please input a city name!")

unit = st.selectbox("Select Temperature Unit", ("Celsius", "Fahrenheit"))
g_type = st.selectbox("Select Graph Type", ("Line Graph", "Bar Graph"))

unit_c = 'metric' if unit == 'Celsius' else 'imperial'

def get_weather_data(city):
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units={unit_c}'
    response = requests.get(url)
    return response.json()

def plot_temperatures_line(temp_min, temp_max):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=["Min Temp", "Max Temp"], y=[temp_min, temp_max], name='Temperatures'))
    return fig

def plot_temperatures_bar(temp_min, temp_max):
    fig = go.Figure(
        data=[
            go.Bar(name='Minimum Temperature', x=["Min Temp"], y=[temp_min]),
            go.Bar(name='Maximum Temperature', x=["Max Temp"], y=[temp_max])
        ]
    )
    fig.update_layout(barmode='group')
    return fig

def display_weather(city):
    data = get_weather_data(city)
    if data.get("cod") != 200:
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
    if 'weather' in data:
        st.title("Impending Weather Alerts:")
        # You can use the 'weather' list to check for specific conditions like rain, fog, etc.
        for weather in data['weather']:
            if weather['main'].lower() in ['rain', 'storm', 'snow']:
                st.write(f"### {weather['main']} Alert!")

if __name__ == '__main__':
    if place:
        display_weather(place)
        updates(place)
