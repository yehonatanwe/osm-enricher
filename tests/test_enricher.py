from copy import deepcopy
from enricher import enrich_data


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
    "Latitude": -47.797,
    "Longitude": 43.9051,
    "Address": "9 Lynch St 3011, Melbourne, Australia"
}]


def test_enrich_data():
    enrich_data(DATA)
    assert 'School Count' in DATA[0]
