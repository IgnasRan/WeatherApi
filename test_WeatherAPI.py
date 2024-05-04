import unittest
import WeatherAPI
import random


class TestWeatherAPI(unittest.TestCase):
    def setUp(self):
        self.decorator = WeatherAPI.WeatherInfoDecorator()
        self.real_time = WeatherAPI.RealtimeWeather()
        self.forecast = WeatherAPI.ForecastWeather()
        self.astronomy = WeatherAPI.Astronomy()
        self.real_time_info = WeatherAPI.RealtimeWeatherInfo()
        self.forecast_info = WeatherAPI.ForecastWeatherInfo()
        self.astronomy_info = WeatherAPI.AstronomyInfo()
        self.user_input_good = ["Vilnius", "London", "Tokyo", "New York", "Paris", "Beijing", "Moscow", "Sydney",
                                "Cairo",   "Rio de Janeiro", "Istanbul", "Mumbai", "Rome", "Los Angeles", "Dubai",
                                "Buenos Aires", "Amsterdam"]
        self.user_input_good_length = len(self.user_input_good)

    def test_get_real_time_info_good(self):
        for index in range(self.user_input_good_length):
            self.assertTrue(self.real_time_info.tidy_up_info(self.real_time.get_info(self.user_input_good[index])))

    def test_get_forecast_info_good(self):
        for index in range(self.user_input_good_length):
            self.assertTrue(self.forecast_info.tidy_up_info(self.forecast.get_info(self.user_input_good[index],
                                                                                   random.randint(1, 3))))

    def test_get_astronomy_info_good(self):
        for index in range(self.user_input_good_length):
            self.assertTrue(self.astronomy_info.tidy_up_info(self.astronomy.get_info(self.user_input_good[index])))


if __name__ == "__main__":
    unittest.main()
