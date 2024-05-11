
# WeatherApi
# By Ignas Ranonis EAf-23
## Description
A WeatherApi program which prints information from https://rapidapi.com/weatherapi/api/weatherapi-com/ based on given options

## Features

- A program to chech on current weather or the forecast of up to 3 days.
- "input.json" file with 17 different cities.
- "output.json" file to preview the previous or current results of the program.
- "test_WeatherApi" program to test the main program's functionality


## How to run the program
To run the program you will need to install Python version 3.x and the "requests" library.
## Usage
The program is ran through the terminal. The cities are selected from the "input.json" file, in which there are given 17 different cities to choose from. When the program is started you will be given 6 options:\
    1. "Current weather" - gives information about the current weather in a selected city.\
    2. "Weather forecast - gives a 1 to 3 day forecast of a selected city (The number of   days will need to be written in the terminal).\
    3. "Astronomy information - gives sunrise, sunset, moonrise and moonset times in a selected city.\
    4. "Run all (1st, 2nd and 3rd options) - runs all 3 previously mentioned options.\
    5. "Next city" - selects the next city in the "input.json" file.\
    6. "Exit" - exits the program.

All results will be written into the "output.json" file.
## Code analysis
#### The program has 4 object-oriented programming pillars: 
- Polymorphism - it is achieved by using get_info method in the main class and it's subclasses, it is
    overridden in each subclass to provide different functionality by accepting different parameters.
- Abstraction is achieved by using abstract method get_info in the abstract class Weather, 
    forcing the child classes to implement the method.
- Encapsulation is achieved by defining the __headers and __url as private attributes in the abstract class Weather.
- Inheritance is achieved by using the ABC module to create an abstract class Weather which is then also inherited by subclasses.
#### Code example of previously mentioned pillars:
        class Weather(ABC): #Use of Inheritance
            def __init__(self):
            self.__headers = {
                "X-RapidAPI-Key": "b6304749c9msh3932623f6c02d43p11c447jsnb9059f998285",
                "X-RapidAPI-Host": "weatherapi-com.p.rapidapi.com"}
            self.__url = "https://weatherapi-com.p.rapidapi.com/"  #__url and __headers vairables show the use of Encapsulation

            @abstractmethod #Use of Abstraction
            def get_info(self, *args):
                response = requests.get(self.__url + args[0], headers=self.__headers, params=args[1])
                response.raise_for_status()

                return response.json()


        class RealtimeWeather(Weather):
            def get_info(self, *args):
                endpoint = "current.json"
                params = {"q": args[0]}

                return super().get_info(endpoint, params)


        class ForecastWeather(Weather):
            def get_info(self, *args):
                endpoint = "forecast.json"
                params = {"q": args[0], "days": args[1]}

                return super().get_info(endpoint, params)


        class Astronomy(Weather):
            def get_info(self, *args):
                endpoint = "astronomy.json"
                params = {"q": args[0]}

                return super().get_info(endpoint, params)

#### There are 2 types of design patterns used:
- Singleton pattern is implemented by creating a single instance of the class JsonFileWriter. "__new" method is overridden to check if the instance already exists, if it does not, it creates a new instance, if it does exist, it returns the existing instance, hence ensuring only one instance is created - Singleton pattern. This class is also responsible for reading and writing from or into .json file format.

        class JsonFileWriterReader:
        _instance = None

            def __new__(cls, file_path_output, file_path_input):
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._file_path_output = file_path_output
                    cls._instance._file_path_input = file_path_input
                return cls._instance

            def write_to_json(self, json_data):
                try:
                    with open(self._file_path_output, 'r+') as file:
                        try:
                            existing_data = json.load(file)
                        except json.JSONDecodeError:
                            existing_data = []

                        existing_data.append(json_data)
                        file.seek(0)
                        json.dump(existing_data, file, indent=4)
                        file.truncate()
                except FileNotFoundError:
                    with open(self._file_path_output, 'w') as file:
                        json.dump([json_data], file, indent=4)

            def read_from_json(self):
                try:
                    with open(self._file_path_input, 'r') as file:
                        data = json.load(file)
                        return data['Input']
                except FileNotFoundError:
                    print("File doesn't exist or no data found in the file.")

- Decorator pattern is implemented by creating a decorator class WeatherInfoDecorator, which is inherited by the classes RealtimeWeatherInfo, ForecastWeatherInfo and AstronomyInfo. The decorator class has a write_info method which is overridden by the child classes to provide different functionality.

        class WeatherInfoDecorator:
            def tidy_up_info(self, data):
                pass


        class RealtimeWeatherInfo(WeatherInfoDecorator):
            def tidy_up_info(self, data):
                real_time_info_json = {
                    "API": "Real time weather information of " + data['location']['name'],
                    "Temperature": data['current']['temp_c'],
                    "Condition": data['current']['condition']['text'],
                    "Wind": data['current']['wind_kph'],
                    "Wind direction": data['current']['wind_dir'],
                    "Temperature feels like": data['current']['feelslike_c']
                }

                print(json.dumps(real_time_info_json, indent=4))
                return real_time_info_json


        class ForecastWeatherInfo(WeatherInfoDecorator):
            def tidy_up_info(self, data):
                forecast_info_json = {"API": "Forecast information of " + data['location']['name']}
                day = 0
                while day < len(data['forecast']['forecastday']):
                    forecast_weather_json = {
                        "Date": data['forecast']['forecastday'][day]['date'],
                        "Max temperature": data['forecast']['forecastday'][day]['day']['maxtemp_c'],
                        "Min temperature": data['forecast']['forecastday'][day]['day']['mintemp_c'],
                        "Condition": data['forecast']['forecastday'][day]['day']['condition']['text']
                    }
                    forecast_info_json.update({f"Day {day + 1}": forecast_weather_json})
                    day += 1

                print(json.dumps(forecast_info_json, indent=4))
                return forecast_info_json


        class AstronomyInfo(WeatherInfoDecorator):
            def tidy_up_info(self, data):
                astronomy_info_json = {
                    "API": "Astronomy information of " + data['location']['name'],
                    "Sunrise": data['astronomy']['astro']['sunrise'],
                    "Sunset": data['astronomy']['astro']['sunset'],
                    "Moonrise": data['astronomy']['astro']['moonrise'],
                    "Moonset": data['astronomy']['astro']['moonset'],
                }

                print(json.dumps(astronomy_info_json, indent=4))
                return astronomy_info_json


## Test cases
Each case of the "TestWeatherAPI" class tests the functionality of a certain aspect of the Weather API integration, such as retrieving current weather information, forecasting weather conditions for specific durations, and obtaining astronomy data like sunrise and sunset times for given locations.

    class TestWeatherAPI(unittest.TestCase):
        def setUp(self):
            # creation of instances
            self.user_input_good = ["Vilnius", "London", "Tokyo", "New York", "Paris", "Beijing", "Moscow", "Sydney",
                                    "Cairo",   "Rio de Janeiro", "Istanbul", "Mumbai", "Rome", "Los Angeles", "Dubai",
                                    "Buenos Aires", "Amsterdam"]
            self.user_input_good_length = len(self.user_input_good)

        def test_get_real_time_info_good(self):
            for i in range(self.user_input_good_length):
                self.assertTrue(self.real_time_info.tidy_up_info(self.real_time.get_info(self.user_input_good[i])))

        def test_get_forecast_info_good(self):
            for i in range(self.user_input_good_length):
                self.assertTrue(self.forecast_info.tidy_up_info(self.forecast.get_info(self.user_input_good[i],
                                                                                    random.randint(1, 3))))

        def test_get_astronomy_info_good(self):
            for i in range(self.user_input_good_length):
                self.assertTrue(self.astronomy_info.tidy_up_info(self.astronomy.get_info(self.user_input_good[i])))

## Results
#### There were a few challenges i had to face while creating the program:
- It was quite challenging to include all four used OOP pillars into the program.
- Reading and writing into .json file format was new to me, therefore had to be learnt and implimented correclty.
- Requesting information from an API was also new to me, it was in some way a challenge i have given myself to make the project more interesting and beneficial.
## Conclusion
In conclusion, I encountered various challenges that allowed me to deepen my understanding of object-oriented programming principles, particularly encapsulation, inheritance, polymorphism, and abstraction. I also learned to read from and write to JSON files, request information from an API. All of this has given me some valuable experience and expanded my skill set. Successfully implementing these features has enhanced the functionality and usability of the program.
