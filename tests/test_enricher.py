from random import uniform

import pytest

from osm_enricher.enricher import enrich_data, find_enrichment

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
NODES = [
    {'tag': [{'k': 'amenity', 'v': 'school'}, {'k': 'amenity', 'v': 'foo'}]},
    {'tag': [{'k': 'amenity', 'v': 'school'}]},
    {'tag': [{'k': 'amenity', 'v': 'bar'}]},
    {'tag': {'k': 'amenity', 'v': 'bar'}}
]


@pytest.mark.parametrize(
    argnames=['data'],
    argvalues=[
        [[{}]],
        [[{k: v for k, v in DATA[0].items() if k != 'Latitude'}]]
    ]
)
def test_enrich_invalid_data(data):
    with pytest.raises(Exception):
        enrich_data(data=data)


@pytest.mark.parametrize(
    argnames=['latitude', 'longitude'],
    argvalues=[
        [DATA[0]['Latitude'],  DATA[0]['Longitude']],
        [uniform(-90, 90), uniform(-180, 180)],
        [uniform(-90, 90), uniform(-180, 180)],
        [uniform(-90, 90), uniform(-180, 180)]
    ]
)
def test_enrich_random_valid_data(latitude, longitude):
    DATA[0]['Latitude'] = latitude
    DATA[0]['Longitude'] = longitude
    enrich_data(data=DATA)
    assert 'SchoolCount' in DATA[0]


@pytest.mark.parametrize(
    argnames=['data', 'enrichments'],
    argvalues=[
        [NODES, 2],
        [NODES[:2], 2],
        [[NODES[0]], 1],
        [[NODES[1]], 1],
        [NODES[2:], 0]
    ]
)
def test_find_enrichment_valid_data(data, enrichments):
    assert enrichments == find_enrichment(data=data)


@pytest.mark.parametrize(
    argnames=['data'],
    argvalues=[
        [[{'tag': 'foobar'}]],
        [[{'tag': {'k': 'foo'}}]],
        [[{'tag': {'v': 'bar'}}]],
        [[{'tag': [{'v': 'bar'}]}]],
        [[{'tag': [{'k': 'foo', 'v': 'bar'}, {'k': 'foo'}]}]],
    ]
)
def test_find_enrichment_invalid_tags(data):
    with pytest.raises(Exception):
        find_enrichment(data=data)
