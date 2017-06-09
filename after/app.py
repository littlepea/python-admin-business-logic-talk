import urllib2
import json

from aqi import Station
from cache import cache


API_BASE = 'https://api.openaq.org/v1/latest'


def _get_city_url(city):
    return '{}?city={}'.format(API_BASE, city)


def _load_results(url):
    try:
        response = urllib2.urlopen(url)
        results = json.load(response)
        return results['results']
    except urllib2.HTTPError, e:
        return []


def _get_station_pm25(station):
    for measurement in station['measurements']:
        if measurement['parameter'] == 'pm25':
            return measurement['value']


@cache
def get_stations(city):
    return [
        Station(
            name=result['location'],
            pm25=_get_station_pm25(result))
        for result in _load_results(_get_city_url(city))
    ]


def get_recommendation(level):
    if level.indoors:
        return 'Please, stay indoors with purified air.'

    if level.mask:
        return 'Please, wear a mask if going out.'

    return 'Feel free to go out!'
