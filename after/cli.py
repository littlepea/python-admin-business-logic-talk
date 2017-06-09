"""
This script displays air quality information for a specific city.
"""
import argparse

from app import get_stations, get_recommendation
from aqi import aqi_level, city_aqi


def main(city):
    print('\nChecking air quality for {}...\n'.format(city))

    stations = get_stations(city)

    if not stations:
        print('No stations found in {}'.format(city))
        return

    level = aqi_level(city_aqi(stations))
    recommendation = get_recommendation(level)

    print('The air in {} is {} ({})'.format(city, level.name, level.aqi))
    print(recommendation)


if __name__ == "__main__":
    # Parse CLI arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("city", help="Name of the city")
    arguments = parser.parse_args()

    # Run the program
    main(arguments.city)
