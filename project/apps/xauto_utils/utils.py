import urllib2, urllib
import math

from django.core.cache import cache
from django.conf import settings
from django.utils import simplejson as json


def search_places(address, real_address, coords, selectable_only=False):
    from placeforpeople.places.models import Place
    from django.db.models import Q

    real_address = real_address.split(',')[0] # to prevent things like 'Illinois, United States'

    name_places = Place.objects.filter(name__iexact=real_address)
    if not len(name_places):
        name_places = Place.objects.filter(name__iexact=address)

    if len(name_places):
        place_ids = [p.id for p in name_places]
        places_q = Q(id__in=place_ids)
        for place in name_places:
            places_q |= place.inner_places_q()

        strids = str(tuple(place_ids)).replace(',)', ')')
        if selectable_only:
            return (Place.objects
                    .filter(places_q, is_selectable_for_campaigning=True)
                    .extra(select={
                        'name_match': 'places_place.id in %s' % strids,
                    })
                    .order_by('-name_match', '-is_admin', 'name'))
        else:
            return (Place.objects
                                .filter(places_q)
                                .extra(select={
                                    'name_match': 'places_place.id in %s' % strids,
                                })
                                .order_by('-name_match', '-is_admin', 'name'))

    bbox = poly_from_4_coords(reduce=20, *coords)
    if selectable_only:
        return (Place.objects.filter(geopoly__intersects=bbox, is_selectable_for_campaigning=True)
                .order_by('-is_admin', 'name'))
    else:
        return (Place.objects.filter(geopoly__intersects=bbox)
                        .order_by('-is_admin', 'name'))



# Canada 0.224661367694
# Russia 0.341751106958
# United States 0.154385007851

exceptions = {
#    'Russia': 0.3,
#    'Canada': 0.22,
    'Texas': 0.013,
}

def convert_to_one_poly(geom):
    if isinstance(geom, Polygon) and len(geom) > 1:
        return Polygon(sorted(geom, key=len, reverse=True)[0])

    return geom

def simplify_polygon(geom, simplification, name, max_tolerance=5):
    max_tolerance = max_tolerance or 0.25

    max_area = simplification * max_tolerance
    normalized_area = max_area * math.tanh (geom.area / max_area)
    tolerance = normalized_area / simplification

    if name in exceptions:
       tolerance = exceptions[name]

    geom = geom.simplify(tolerance, preserve_topology=True)

    if geom.geom_type == 'MultiPolygon':
        polygons = [p for p in geom]
        polygons.sort(key=lambda p: p.area, reverse=True)
        return convert_to_one_poly(polygons[0])
    elif geom.geom_type == 'Polygon':
        return convert_to_one_poly(geom)
    else:
        raise Exception('Unknown geom_type: ', geom.geom_type)

def get_tile(lat, lng, zoom):
    x = (lng + 180.0) / (360.0 / 2 ** zoom)
    y = (lat + 85.0) / (170.0 / 2**zoom)
    return int(x), int(y)


def clear_map_cache(polygon):
    bbox = polygon.envelope

    def min_max_tiles(zoom):
        tiles = [get_tile(p[1], p[0], zoom) for p in bbox[0]]
        min_x = min([t[0] for t in tiles])
        min_y = min([t[1] for t in tiles])
        max_x = max([t[0] for t in tiles])
        max_y = max([t[1] for t in tiles])
        return min_x, min_y, max_x, max_y

    def possible_rectangles(width, height, zoom, min_x, min_y, max_x, max_y):
        res = []
        for x in range(min_x - width, max_x + width):
            for y in range(min_y - height, max_y + height):
                res.append([x, y, x + width, y + height, zoom])
        return res

    for zoom in range(1, 9):
        min_max = min_max_tiles(zoom)
        for width in range(1, 4):
            for height in range(1, 4):
                rects = possible_rectangles(width, height, zoom, *min_max)
                for rect in rects:
                    str_rect = [str(coord) for coord in rect]
                    cache.delete(':'.join(['map', 'area'] + str_rect))

def geocode(address):
    address = urllib.quote(address)
    query = urllib.urlencode({
        'q': address,
        'sensor': False,
        'output': 'json',
        'oe': 'utf8',
        'key': getattr(settings, 'GOOGLE_MAPS_API_KEY', ''),
    })
    url='http://maps.google.com/maps/geo?' +query
    response = urllib2.urlopen(url)
    json_geocode = response.read()
    return json.loads(json_geocode)

def geocode_place(address):
    """
    Geocode any kind of provided address and try to return info about real 
    geo placemark. 
    
    @type    address: string
    @param   address: String which may contain full address or part of it.
    
    @rtype: Place, None
    @return: Place object if geocode was successful, otherwise None
    """
    from placeforpeople.places.forms import GeocoderResultForm
    
    address = address.replace(' ', '-')

    res = geocode(address)
    if res['Status']['code'] != 200 or len(res['Placemark']) == 0:
        return None
    pm = res['Placemark'][0]
    box = pm['ExtendedData']['LatLonBox']

    reduce = 25
    dy = (box['north'] - box['south']) / 100 * reduce / 2
    dx = (box['east'] - box['west']) / 100 * reduce / 2

    placemark_info = {
        'name': address,
        'real_name': pm['address'].split(',')[0],
        'south': box['south'] + dy,
        'north': box['north'] - dy,
        'east': box['east'] - dx,
        'west': box['west'] + dx,
    }
    form = GeocoderResultForm(placemark_info)
    if form.is_valid():
        return form.get_place()
    return None


def poly_from_tiles(x, y, x1, y1, zoom):
    if '.' in x or '.' in y or '.' in x1 or '.' in y1:
        x, y, x1, y1, zoom = float(x), float(y), float(x1), float(y1), int(zoom)
        return Polygon.from_bbox([x, y, x1, y1])
    else:
        x, y, x1, y1, zoom = int(x), int(y), int(x1), int(y1), int(zoom)
        return Polygon.from_bbox([
            x * (360.0 / 2 ** zoom) - 180,
            y * (170.0 / 2 ** zoom) - 85,
            min((x1 + 1) * (360.0 / 2 ** zoom) - 180, 179),
            min((y1 + 1) * (170.0 / 2 ** zoom) - 85, 85),
        ])

def poly_from_4_coords(north, south, east, west, reduce=0):
    dy = (north - south) / 100 * reduce / 2
    dx = (east - west) / 100 * reduce / 2
    return Polygon.from_bbox([east - dx, north - dy, west + dx, south + dy])

def country_codes_for_EU():
    return [
        'AT', #Austria
        'BE', #Belgium
        'BG', #Bulgaria
        'CY', #Cyprus
        'CZ', #Czech Republic
        'DK', #Kingdom of Denmark
        'EE', #Republic of Estonia
        'FI', #Republic of Finland
        'FR', #French Republic
        'DE', #Federal Republic of Germany
        'GR', #Hellenic Republic
        'HU', #Hungary
        'IE', #Ireland
        'IT', #Italian Republic
        'LV', #Republic of Latvia
        'LT', #Republic of Lithuania
        'LU', #Grand Duchy of Luxembourg
        'MT', #Malta
        'NL', #Kingdom_of_the_Netherlands
        'PL', #Poland
        'PT', #Portuguese Republic
        'RO', # Romania
        'SK', # Slovak Republic
        'SI', #Slovenia
        'ES', #Spain
        'SE', #Sweden
    ]


def form_up_places_list(places, correct_sublevel=0, movement=None):
    from places.models import Place
    result = []
    if movement is not None:
        advocated_places_list = movement.places.all()

    for x in places:
        if type(x) is Place:
            if movement is None:
                if x.sublevel_count()-correct_sublevel>=0:
                    result.append({
                        'id': x.id,
                        'full_name': x.full_name,
                        'get_absolute_url': x.get_absolute_url(),
                        'sublevel_count': x.sublevel_count()-correct_sublevel
                    })
            else:
                result.append({
                    'id': x.id,
                    'full_name': x.full_name,
                    'get_absolute_url': x.get_absolute_url(),
                    'advocated' : x in advocated_places_list
                })

    if movement:
        return sorted(result, key=lambda x: x['full_name'])
    return result