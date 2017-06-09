"""
This script displays air quality information for a specific city.
"""
import argparse
import urllib2
import json

from aqi import Station, city_aqi, aqi_level


API_BASE = 'https://api.openaq.org/v1/latest'
CACHE = {}


def main(city):
    print('\nChecking air quality for {}...\n'.format(city))

    # Check cache
    stations = CACHE.get(city, [])

    if not stations:
        try:
            # Call the API
            url = '{}?city={}'.format(API_BASE, city)
            response = urllib2.urlopen(url)
            results = json.load(response)
            for result in results['results']:
                pm25 = None
                for measurement in result['measurements']:
                    if measurement['parameter'] == 'pm25':
                        pm25 = measurement['value']

                stations.append(Station(
                    name=result['location'],
                    pm25=pm25))

            # Write to cache
            CACHE[city] = stations
        except urllib2.HTTPError, e:
            print('Could not retrieve results from the server: {}'.format(e))
            return

    if not stations:
        print('No stations found in {}'.format(city))
        return

    level = aqi_level(city_aqi(stations))

    # Display the AQI level to the user
    print('The air in {} is {} ({})'.format(
        city,
        level.name,
        level.aqi
    ))

    if level.indoors:
        print('Please, stay indoors with purified air.')
    elif level.mask:
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
