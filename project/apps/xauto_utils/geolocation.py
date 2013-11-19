#from django.contrib.gis.utils import GeoIP


def user_location(request):
    return  {
        'city': 'San Francisco',
        'latitude': 37.4419,
        'longitude': -122.1419,
    }
