import requests
import json

API = "eef1c80c1154b64315081e125d5a37d6"
locationData = {}
fav_cities_file = "favorite_cities.json"

"""This Python program comprises of 4 functions

    1. saved_cities() --> this function will read the json file where the favorited cities are listed in a json data format
    2. save_cities() --> this function will write data stored in the fav_cities variable 
    3. coordinates() --> this function will take a city name and output the longitude and latitude of the city so it can be used in the weather_call() function
    4. weather_call() --> this function will take the longitude and latitude from the coordinates() function and output the weather of the particular coordinates
"""

def saved_cities():
    """ This function fetch the list of Favorited Cities"""
    with open(fav_cities_file, "r") as file:
            return json.load(file)
   
    

def save_cities(fav_cities):
    """This function saves the list of Favorited Cities"""
    with open(fav_cities_file, "w") as file:
        json.dump(fav_cities,file)

def coordinates(name):
        """This function will get the longitude and latitude of the city using the Geolocaton API"""        
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
    """This function will get weather of the city"""
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

    """Here is the start of the menu"""
    print("Weather Application:")
    print("1. Add a city to you favorite list")
    print("2. View favorited cities' weathers")
    print("3. Exit Application")
    option = input("Choose one of the options: ")
    
    if option == "1":

        """If the option 1 is choosen then the program will first check if there are more than 3 cities in the list"""

        if len (fav_cities) >=3:
            print("Maximum 3 cities allowed, remove a city")
            for i in fav_cities:
                print(f"  {i}")

            """If there are more then 3 cities in the file then the program will prompt the user to remove a city"""

            remove_city = input("Type the name of the city to remove: ")
            fav_cities.remove(remove_city)
            save_cities(fav_cities)
        
        """After the max capacity problem is resolved the program will move forward to add a city in the favorites list """

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
        """If the option 2 is choosen then the program output the weather for the cities"""
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
        """If the option 3 is choosen it will end the program"""
        print("Ending Program")
    else: 
        print("Invalid Option")
   

if __name__ == '__main__':
    main()