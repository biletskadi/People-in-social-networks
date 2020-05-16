import mapbox
import json

geocoder = mapbox.Geocoder(access_token='...')
response = geocoder.forward('Paris, France')
with open('text.json', 'w', encoding='UTF-8') as f:
    json.dump(response.json(), f)

from mapbox import Directions
resp = Directions('mapbox.driving').directions([origin, destination])
driving_routes = resp.geojson()
first_route = driving_routes['features'][0]
