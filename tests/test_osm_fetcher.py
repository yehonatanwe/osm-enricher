from osm_enricher.osm_fetcher import fetch_osm_data
from osm_enricher.exceptions import osm_fetcher_exceptions


def test_fetch_osm_valid_data():
    nodes = fetch_osm_data(-37.797, 144.9051)
    assert isinstance(nodes['osm'].get('way'), list)


def test_fetch_osm_invalid_data():
    try:
        fetch_osm_data(None, None)
    except Exception as e:
        assert osm_fetcher_exceptions.MISSING_FIELDS_ERROR in str(e)


def test_fetch_osm_invalid_coordinates():
    try:
        fetch_osm_data(81, 180)
    except Exception as e:
        assert osm_fetcher_exceptions.FAILED_RETRIEVE_ERROR[:-2] in str(e)
