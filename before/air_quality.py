"""
This script displays air quality information for a specific city.
"""
import argparse
import urllib2
import json

from collections import OrderedDict


API_BASE = 'https://api.openaq.org/v1/latest'

AQI_LEVELS = OrderedDict({
    51:	{
        'range': '0-50',
        'level': 'Good'
    },
    101: {
        'range': '51-100',
        'level': 'Moderate'
    },
    151: {
        'range': '101-150',
        'level': 'Unhealthy for Sensitive Groups'
    },
    201: {
        'range': '151-200',
        'level': 'Unhealthy',
        'mask': True
    },
    301: {
        'range': '201-300',
        'level': 'Very Unhealthy',
        'maks': True
    },
    10000: {
        'range': '300+',
        'level': 'Hazardous',
        'indoors': True
    }
})


CACHE = {}


def main(city):
    print('\nChecking air quality for {}...\n'.format(city))

    # Check cache
    stations = CACHE.get(city)

    if not stations:
        try:
            # Call the API
            url = '{}?city={}'.format(API_BASE, city)
            response = urllib2.urlopen(url)
            results = json.load(response)
            stations = results['results']

            # Write to cache
            CACHE[city] = stations
        except urllib2.HTTPError, e:
            print('Could not retrieve results from the server: {}'.format(e))
            return

    if not stations:
        print('No stations found in {}'.format(city))
        return

    # Get PM2.5 values from all stations
    pm25 = [
        measurement['value']
        for station in stations
        for measurement in station['measurements']
        if measurement['parameter'] == 'pm25'
    ]

    # Calculate average PM2.5
    average_pm25 = sum(pm25, 0.0) / len(pm25)

    # Find the right AQI level
    aqi = None
    for ceiling, level in AQI_LEVELS.items():
        if average_pm25 < ceiling:
            aqi = level
            break

    # Display the AQI level to the user
    print('The air in {} is {} ({})'.format(
        city,
        aqi['level'],
        average_pm25
    ))

    if aqi.get('indoors'):
        print('Please, stay indoors with purified air.')
    elif aqi.get('mask'):
        print('Please, wear a mask if going out.')
    else:
        print('Feel free to go out!')


if __name__ == "__main__":
    # Parse CLI arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("city", help="Name of the city")
    arguments = parser.parse_args()

    # Run the program
    main(arguments.city)
