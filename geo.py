import json
from common import table, table_geo, google_api_key
from pprint import pprint
import requests

URL = 'https://maps.googleapis.com/maps/api/geocode/json'

SEEN = {}


def revcode(row):
    lat, lng = row.get('latitude'), row.get('longitude')
    latlng = '%s,%s' % (lat, lng)
    table.update({
        'case_id': row['case_id'],
        'latlng': latlng
    }, ['case_id'])
    if table_geo.find_one(latlng=latlng):
        return
    res = requests.get(URL, params={
        'latlng': latlng,
        'key': google_api_key
    })
    data = res.json()
    geo = {
        'latlng': latlng,
        'data': json.dumps(data)
    }
    if len(data['results']):
        result = data['results'][0]
        for result in data['results']:
            for comp in result.get('address_components', []):
                t = comp['types']
                v = comp['short_name']
                if 'country' in t:
                    geo['country'] = v
                if 'administrative_area_level_2' in t:
                    geo['adm_2'] = v
                if 'administrative_area_level_3' in t:
                    geo['adm_3'] = v
                if 'route' in t:
                    geo['route'] = v
    table_geo.upsert(geo, ['latlng'])
    print geo['latlng']


def revcode_all():
    for row in table:
        revcode(row)


if __name__ == '__main__':
    revcode_all()
