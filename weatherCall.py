import requests
API = "eef1c80c1154b64315081e125d5a37d6"
locationData = {}

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
def weather_call(name):
    
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={locationData['lat']}&lon={locationData['lon']}&appid={API}"
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
    city = input("City Name: ")
    coordinates(city)
    result = weather_call(city)

    if result:
        print(result)
    else:
        print('Failed to fetch posts from API.')

if __name__ == '__main__':
    main()