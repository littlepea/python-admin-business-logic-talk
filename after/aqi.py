from collections import OrderedDict, namedtuple


Station = namedtuple('Station', ['name', 'pm25'])
Level = namedtuple('Level', ['name', 'aqi', 'mask', 'indoors'])


AQI_LEVELS = OrderedDict()
AQI_LEVELS[51] = {
    'range': '0-50',
    'level': 'Good'
}
AQI_LEVELS[101] = {
    'range': '51-100',
    'level': 'Moderate'
}
AQI_LEVELS[151] = {
    'range': '101-150',
    'level': 'Unhealthy for Sensitive Groups'
}
AQI_LEVELS[201] = {
    'range': '151-200',
    'level': 'Unhealthy',
    'mask': True
}
AQI_LEVELS[301] = {
    'range': '201-300',
    'level': 'Very Unhealthy',
    'maks': True
}
AQI_LEVELS[10000] = {
    'range': '300+',
    'level': 'Hazardous',
    'indoors': True
}


def median(numbers):
    return (sorted(numbers)[int(round((len(numbers) - 1) / 2.0))] +
            sorted(numbers)[int(round((len(numbers) - 1) // 2.0))]) / 2.0


def city_aqi(stations):
    pm25 = [station.pm25 for station in stations]
    return median(pm25)


def aqi_level(aqi):
    for ceiling, level in AQI_LEVELS.items():
        if aqi < ceiling:
            return Level(
                name=level['level'],
                aqi=aqi,
                mask=level.get('mask', False),
                indoors=level.get('indoors', False)
            )
