from enricher import enrich_data
from exceptions import enricher_exceptions
from random import uniform


DATA = [{
    "Suburb": "Footscray",
    "Rooms": 3,
    "Date": "2016-03-12",
    "Postcode": 3011,
    "Bedroom2": 3,
    "Bathroom": 1,
    "Car": 1,
    "Landsize": 292,
    "YearBuilt": 1900,
    "Latitude": -37.797,
    "Longitude": 144.9051,
    "Address": "9 Lynch St 3011, Melbourne, Australia"
}]


def test_enrich_preset_valid_data():
    enrich_data(DATA)
    assert DATA[0]['SchoolCount'] == 5


def test_enrich_cache():
    enrich_data(DATA)
    first = DATA[0]['SchoolCount']
    enrich_data(DATA)
    second = DATA[0]['SchoolCount']
    assert first == second


def test_enrich_empty_data():
    try:
        enrich_data({})
        assert False
    except Exception as e:
        assert enricher_exceptions.MISSING_DATA_ERROR in str(e)


def test_enrich_invalid_data():
    DATA[0].pop('Latitude')
    try:
        enrich_data(DATA)
        assert False
    except Exception as e:
        assert enricher_exceptions.MISSING_DATA_ERROR in str(e)


def test_enrich_random_valid_data():
    DATA[0]['Latitude'] = uniform(-90, 90)
    DATA[0]['Longitude'] = uniform(-180, 180)
    enrich_data(DATA)
    assert 'SchoolCount' in DATA[0]
