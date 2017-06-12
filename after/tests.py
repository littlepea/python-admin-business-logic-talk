import unittest

from aqi import city_aqi, aqi_level, Station


class CityAqiTest(unittest.TestCase):
    def test_city_aqi(self):
        stations = [Station('s1', 100), Station('s2', 30), Station('s3', 20)]
        self.assertEqual(30, city_aqi(stations))


class AqiLevelTest(unittest.TestCase):
    def test_good_aqi_level(self):
        level = aqi_level(50)
        self.assertEqual('Good', level.name)
        self.assertFalse(level.mask)

    def test_unhealthy_aqi_level(self):
        level = aqi_level(180)
        self.assertEqual('Unhealthy', level.name)
        self.assertTrue(level.mask)

    def test_hazardous_aqi_level(self):
        level = aqi_level(800)
        self.assertEqual('Hazardous', level.name)
        self.assertTrue(level.indoors)
