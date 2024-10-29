import requests
from datetime import datetime, timedelta
import pytz
import folium
import os

API_KEY = "331e8e1033c9a5ed77d4105a9ae89494"  
country = input("Enter Country Name: ")
city = input("Enter City Name: ")
geocoding_url = f"http://api.openweathermap.org/data/2.5/weather?q={city},{country}&appid={API_KEY}"

try:
    response = requests.get(geocoding_url)
    response.raise_for_status()  
    data = response.json()
    
    if data.get('cod') != 200:
        print("City not found. Please check the name and try again!")
    else:
        lat = data['coord']['lat']
        lon = data['coord']['lon']
        state = data.get('sys', {}).get('state', None)
        url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
        
        response = requests.get(url)
        response.raise_for_status()  
        data = response.json()

        temperature = data['main']['temp']
        description = data['weather'][0]['description']
        timezone_offset = data['timezone'] 
        country_time = datetime.now(pytz.utc) + timedelta(seconds=timezone_offset)
        india_time = datetime.now(pytz.timezone('Asia/Kolkata'))

        # Get current day
        current_day = country_time.strftime('%A') 
        print(f"Weather in {city}, {'N/A' if state is None else state}, {country}:")
        print(f"Temperature: {temperature}°C")
        print(f"Condition: {description.capitalize()}")
        print(f"Current time in {country}: {country_time.strftime('%Y-%m-%d %I:%M:%S %p')}") 
        print(f"Current time in India: {india_time.strftime('%Y-%m-%d %I:%M:%S %p')}") 
        print(f"Day: {current_day}")
        city_map = folium.Map(location=[lat, lon], zoom_start=10)
        folium.Marker(
            location=[lat, lon],
            popup=f"{city}, {'N/A' if state is None else state}, {country}",
            tooltip='Click for more info'
        ).add_to(city_map)
        folium.Circle(
            location=[lat, lon],
            radius=1000, 
            color='red',
            fill=True,
            fill_color='red',
            fill_opacity=0.5,
            tooltip='Location of the city'
        ).add_to(city_map)
        map_filename = 'city_weather_map.html'
        city_map.save(map_filename)
        print(f"Map has been created and saved as '{os.path.abspath(map_filename)}'.")

except requests.exceptions.RequestException as e:
    print(f"Error: {e}")
