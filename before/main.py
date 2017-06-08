"""
This script displays air quality information for a specific city.
"""
import argparse
import urllib2
import json


API_BASE = 'https://api.openaq.org/v1/latest'

AQI_LEVELS = {
    51:	{
        'range': '0-50',
        'level': 'Good',
        'health': 'Air quality is considered satisfactory, and air pollution poses little or no risk',
        'caution': ''
    },
    101: {
        'range': '51-100',
        'level': 'Moderate',
        'health': 'Air quality is acceptable; however, for some pollutants there may be a moderate health concern '
                  'for a very small number of people who are unusually sensitive to air pollution.',
        'caution': 'Active children and adults, and people with respiratory disease, such as asthma, '
                   'should limit prolonged outdoor exertion.'
    },
    151: {
        'range': '101-150',
        'level': 'Unhealthy for Sensitive Groups',
        'health': 'Members of sensitive groups may experience health effects. '
                  'The general public is not likely to be affected.',
        'caution': 'Active children and adults, and people with respiratory disease, such as asthma, '
                   'should limit prolonged outdoor exertion.'
    },
    201: {
        'range': '151-200',
        'level': 'Unhealthy',
        'health': 'Everyone may begin to experience health effects; '
                  'members of sensitive groups may experience more serious health effects',
        'caution': 'Active children and adults, and people with respiratory disease, such as asthma, '
                   'should avoid prolonged outdoor exertion; '
                   'everyone else, especially children, should limit prolonged outdoor exertion'
    },
    301: {
        'range': '201-300',
        'level': 'Very Unhealthy',
        'health': 'Health warnings of emergency conditions. The entire population is more likely to be affected.',
        'caution': 'Active children and adults, and people with respiratory disease, such as asthma, '
                   'should avoid all outdoor exertion; '
                   'everyone else, especially children, should limit outdoor exertion.'
    },
    10000: {
        'range': '300+',
        'level': 'Hazardous',
        'health': 'Health alert: everyone may experience more serious health effects',
        'caution': 'Everyone should avoid all outdoor exertion'
    }
}


CACHE = {}


def main(arguments):
    # Get city from input
    city = arguments.city
    print('Checking air quality for {}...'.format(city))

    # Check cache
    stations = CACHE.get(city)

    if not stations:
        try:
            # Call the API
            url = '{}?city={}'.format(API_BASE, city)
            response = urllib2.urlopen(url)
            results = json.load(response)
            stations = results['results']
            CACHE[city] = stations
        except urllib2.HTTPError, e:
            print('Could not retrieve results from the server: {}'.format(e))
            return

    if not stations:
        print('No stations found in {}'.format(city))
        return

    # Get PM2.5 values from all stations
    pm25 = []
    for station in stations:
        for measurement in station['measurements']:
            if measurement['parameter'] == 'pm25':
                pm25.append(measurement['value'])

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


if __name__ == "__main__":
    # Parse CLI arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("city", help="Name of the city")
    arguments = parser.parse_args()

    # Run the program
    main(arguments)
