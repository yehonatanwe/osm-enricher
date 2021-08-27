from mock import patch
from pytest import fixture

NODES = {
    'osm': {
        'version': 0.6,
        'generator': 'Overpass API 0.7.56.9 76e5016d',
        'note': {},
        'meta': {'osm_base': '2021-08-27T15:00:03Z'},
        'node': [],
        'way': [
            {
                'id': 29100565,
                'nd': [],
                'tag': [
                    {'k': 'amenity', 'v': 'university'},
                    {'k': 'name', 'v': 'Victoria University (Footscray Nicholson Campus)'},
                    {'k': 'website', 'v': 'https://www.vu.edu.au/campuses-services/our-campuses/footscray-nicholson'}
                ]
            },
            {
                'id': 32920772,
                'nd': [],
                'tag': [
                    {'k': 'amenity', 'v': 'school'},
                    {'k': 'name', 'v': "St Monica's Primary School"},
                    {'k': 'website', 'v': 'www.stmonicasmp.catholic.edu.au'}
                ]
            },
            {
                'id': 33297110,
                'nd': [],
                'tag': [
                    {'k': 'addr:housenumber', 'v': '268-280'},
                    {'k': 'addr:postcode', 'v': 3011},
                    {'k': 'addr:state', 'v': 'VIC'},
                    {'k': 'addr:street', 'v': 'Barkly Street'},
                    {'k': 'addr:suburb', 'v': 'Footscray'},
                    {'k': 'amenity', 'v': 'school'},
                    {'k': 'name', 'v': 'Footscray High School Barkly Campus'},
                    {'k': 'old_name', 'v': 'Gilmore College for Girls'},
                    {'k': 'phone', 'v': '+61 3 9689 4788'},
                    {'k': 'website', 'v': 'https://footscray.vic.edu.au/our-school/barkly-campus-7-9/'},
                    {'k': 'wikidata', 'v': 'Q39048791'}
                ]
            },
            {
                'id': 49130602,
                'nd': [],
                'tag': [
                    {'k': 'amenity', 'v': 'school'},
                    {'k': 'name', 'v': 'Footscray City Primary School'}
                ]
            },
            {
                'id': 291033168,
                'nd': [],
                'tag': [
                    {'k': 'addr:housenumber', 'v': 1},
                    {'k': 'addr:street', 'v': 'Kinnear Street'},
                    {'k': 'amenity', 'v': 'school'},
                    {'k': 'name', 'v': 'Footscray High School Kinnear Campus'},
                    {'k': 'phone', 'v': '+61 3 8387 1500'},
                    {'k': 'website', 'v': 'https://footscray.vic.edu.au/our-school/kinnear-st-campus/'}
                ]
            },
            {
                'id': 512468573,
                'nd': [],
                'tag': [
                    {'k': 'addr:housenumber', 'v': 1},
                    {'k': 'addr:postcode', 'v': 3011},
                    {'k': 'addr:state', 'v': 'VIC'},
                    {'k': 'addr:street', 'v': 'Pilgrim Street'},
                    {'k': 'addr:suburb', 'v': 'Seddon'},
                    {'k': 'amenity', 'v': 'school'},
                    {'k': 'grades', 'v': '7-9'},
                    {'k': 'name', 'v': 'Footscray High School Pilgrim Campus'},
                    {'k': 'note', 'v': 'Junior Secondary School'},
                    {'k': 'operator', 'v': 'Footscray High School'},
                    {'k': 'operator:type', 'v': 'government'},
                    {'k': 'website', 'v': 'https://footscray.vic.edu.au/our-school/pilgrim-campus/'}
                ]
            },
            {
                'id': 779552956,
                'nd': [],
                'tag': [
                    {'k': 'amenity', 'v': 'school'},
                    {'k': 'height', 'v': 3}
                ]
            },
        ],
        'relation': {}
    }
}


@fixture(autouse=True)
def mock_osm_service():
    with patch('osm_enricher.osm_fetcher.get_nodes', return_value=NODES):
        yield
