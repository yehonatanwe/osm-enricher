import pytest

from osm_enricher.osm_fetcher import fetch_osm_data, validate_osm_nodes


def test_osm_fetcher_valid_data():
    nodes = fetch_osm_data(latitude=-37.797, longitude=144.9051)
    assert isinstance(nodes['osm'].get('way'), list)


@pytest.mark.parametrize(
    argnames=['latitude', 'longitude'],
    argvalues=[
        [None, None],
        ['a', 180],
        [80, 'a']
    ]
)
def test_osm_fetcher_invalid_data(latitude, longitude):
    with pytest.raises(Exception):
        fetch_osm_data(latitude=latitude, longitude=longitude)


@pytest.mark.parametrize(
    argnames=['nodes'],
    argvalues=[
        [{}],
        [{'osm': ''}],
        [{'osm': {}}],
    ]
)
def test_validate_osm_nodes(nodes):
    with pytest.raises(Exception):
        validate_osm_nodes(data=nodes)
