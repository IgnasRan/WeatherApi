import requests
from abc import ABC, abstractmethod
import json


'''
Polymorphism is achieved by using get_info method in all classes, it is
overridden in each class to provide different functionality by accepting different parameters.

Abstraction is achieved by using abstract method get_info in the abstract class Weather, 
forcing the child classes to implement the method.

Encapsulation is achieved by defining the headers and url as private attributes in the abstract class Weather

Inheritance is achieved by using the ABC module to create an abstract class Weather
'''


class Weather(ABC):
    def __init__(self):
        self.__headers = {
            "X-RapidAPI-Key": "b6304749c9msh3932623f6c02d43p11c447jsnb9059f998285",
            "X-RapidAPI-Host": "weatherapi-com.p.rapidapi.com"}
        self.__url = "https://weatherapi-com.p.rapidapi.com/"

    @abstractmethod
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


'''
Singleton pattern is implemented by creating a single instance of the class JsonFileWriter

__new__ method is overridden to check if the instance already exists, if it does not, it creates a new instance
if it does, it returns the existing instance, hence ensuring only one instance is created - Singleton pattern
'''


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


'''
Decorator pattern is implemented by creating a decorator class WeatherInfoDecorator,
which is inherited by the classes RealtimeWeatherInfo, ForecastWeatherInfo and AstronomyInfo.

The decorator class has a write_info method which is overridden by the child classes to provide different functionality.
'''


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


if __name__ == "__main__":
    output = JsonFileWriterReader("output.json", "input.json")
    decorator = WeatherInfoDecorator()
    real_time = RealtimeWeather()
    forecast = ForecastWeather()
    astronomy = Astronomy()
    real_time_info = RealtimeWeatherInfo()
    forecast_info = ForecastWeatherInfo()
    astronomy_info = AstronomyInfo()
    user_input = output.read_from_json()
    index = 0

    while True:
        print(f"City: {user_input[index]}")
        user_choice = input("Choose method: \n"
                            "1. Current weather\n"
                            "2. Weather forecast\n"
                            "3. Astronomy information\n"
                            "4. Run All (1, 2, 3)\n"
                            "5. Next city\n"
                            "6. Exit\n"
                            "Enter your choice: ")

        match user_choice:
            case "1":
                try:
                    output.write_to_json(real_time_info.tidy_up_info(real_time.get_info(user_input[index])))
                except requests.exceptions.HTTPError as error:
                    print(f"Error: {error.response.reason}")
            case "2":
                try:
                    while True:
                        days = int(input("Enter a number of days of forecast required (up to 3 days): "))
                        if days < 1 or days > 3:
                            print("Number of days should be between 1 and 3.")
                        else:
                            output.write_to_json(forecast_info.tidy_up_info(forecast.get_info(user_input[index], days)))
                            break
                except ValueError:
                    print("Invalid input. Please enter a valid number.")
                except requests.exceptions.HTTPError as error:
                    print(f"Error: {error.response.reason}")
            case "3":
                try:
                    output.write_to_json(astronomy_info.tidy_up_info(astronomy.get_info(user_input[index])))
                except requests.exceptions.HTTPError as error:
                    print(f"Error:{error.response.reason}")
            case "4":
                try:
                    output.write_to_json(real_time_info.tidy_up_info(real_time.get_info(user_input[index])))

                    while True:
                        days = int(input("Enter a number of days of forecast required (up to 3 days): "))
                        if days < 1 or days > 3:
                            print("Number of days should be between 1 and 3.")
                        else:
                            output.write_to_json(forecast_info.tidy_up_info(forecast.get_info(user_input[index], days)))
                            break

                    output.write_to_json(astronomy_info.tidy_up_info(astronomy.get_info(user_input[index])))
                except requests.exceptions.HTTPError as error:
                    print(f"Error: {error.response.reason}")
            case "5":
                index = index + 1
            case "6":
                exit()
            case _:
                print("Invalid input. Please choose a valid option.")
