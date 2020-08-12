from exceptions import finder_exceptions
from finder import find_enrichment


DATA = [{'tag': [{'k': 'amenity', 'v': 'school'},
                 {'k': 'amenity', 'v': 'foo'}]},
        {'tag': [{'k': 'amenity', 'v': 'school'}]},
        {'tag': [{'k': 'amenity', 'v': 'bar'}]},
        {'tag': {'k': 'amenity', 'v': 'bar'}}]


def test_find_enrichment_valid_data():
    e = find_enrichment(DATA)
    assert e == 2


def test_find_enrichment_invalid_data():
    try:
        find_enrichment(DATA + [{'tag': 'foobar'}])
        assert False
    except Exception as e:
        assert finder_exceptions.UNKNOWN_TAG_STRUCTURE in str(e)


def test_find_enrichment_invalid_tag():
    try:
        find_enrichment(DATA + [{'tag': {'foo': 'bar'}}])
        assert False
    except Exception as e:
        assert finder_exceptions.MISSING_TAG_ATTRIBUTES in str(e)
