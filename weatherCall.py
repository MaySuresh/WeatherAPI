import requests
import json

API = "eef1c80c1154b64315081e125d5a37d6"
locationData = {}
FAV_CITIES_FILE = "favorite_cities.json"

def saved_cities():
    try:
        with open(FAV_CITIES_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []
def save_cities(fav_cities):
    with open(FAV_CITIES_FILE, "w") as file:
        json.dump(fav_cities,file)

def coordinates(name):
        global locationData
        url = f"http://api.openweathermap.org/geo/1.0/direct?q={name}&limit=1&appid={API}"
        try:
             response = requests.get(url)
             if response.status_code == 200:
                  locationKey = response.json()
                  if locationKey:
                         locationData['lat'] = locationKey[-1]["lat"]
                         locationData['lon'] = locationKey[-1]["lon"]
                         return locationData
                  else:
                    print("City Not Found")
                    return None
             else:
                print(f"Error fetching coordinates: {response.status_code}")
                return None
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
            return None
def weather_call(name, lat, lon):
    
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API}"
    try: 
        response = requests.get(url)

        if response.status_code == 200:
              posts=response.json()
              display= f"""
                Weather for {name}, {posts['sys']['country']}
                    - Weather: {posts['weather'][0]['main']}
                    - Temperature: {posts['main']['temp']} K, Feels like: {posts['main']['feels_like']} K
                    - Visiblity: {posts['visibility']} meters
                    - Wind Speed: {posts['wind']['speed']} m/s
                 """
              return display
        else: 
            print("Error:", response.status_code)
            return None
    except requests.exceptions.RequestException as e:
        print('Error:', e)
        return None

def main():
    fav_cities = saved_cities()

    print("Weather Application:")
    print("1. Add a city to you favorite list")
    print("2. View favorited cities' weathers")
    print("3. Exit Application")
    option = input("Choose one of the options: ")
    
    if option == "1":
        city = input("Enter the city's name: ")
        if city not in fav_cities:
            fav_cities.append(city)
            
            print(f"{city} has been added to your favorites.")
            location = coordinates(city)
            if location:
                save_cities(fav_cities)
                weather = weather_call(city, locationData['lat'], locationData['lon'])
                if weather:
                    print(weather)
                else:
                    print(f"Weather not found for {city}")
            else: 
                print(f"Cannot find {city}")
        else:
            print(f"{city} is already in your favorites.")
    elif option == "2":
        if not fav_cities:
            print("You have no favorite cities.")
        else: 
            print("Weather for your favorite cities:")
            for i in fav_cities:
                location = coordinates(i)
                if location:
                    weather = weather_call(i, locationData['lat'], locationData['lon'])
                    if weather:
                        print(weather)
                    else: 
                        print(f"Weather not found for {i}")
                else: 
                    print(f"Cannot find {i}")
    elif option == "3":
        print("Ending Program")
    else: 
        print("Invalid Option")
   

if __name__ == '__main__':
    main()