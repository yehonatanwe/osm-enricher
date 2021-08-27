import logging
from functools import lru_cache
from typing import List

import requests
from lxml.etree import fromstring
from xmljson import XMLData

logger: logging.Logger = logging.getLogger(__name__)
BASE_URL: str = 'http://www.overpass-api.de/api/xapi?*[amenity=*][bbox={}]'


def validate_osm_nodes(data: dict) -> None:
    assert data and isinstance(data, dict) and data.get('osm', {}).get('way'), 'Unexpected OSM nodes structure'


def get_nodes(bounding_box: List[float]) -> dict:
    logger.info('Getting OSM nodes')
    url: str = BASE_URL.format(','.join([str(x) for x in bounding_box]))
    logger.debug(f'OSM request: {url}')

    try:
        response: requests.Response = requests.get(url=url, timeout=60)
    except requests.exceptions.ConnectionError:
        logger.exception(msg='Failed to connect to OSM service')
        raise
    except requests.exceptions.Timeout:
        logger.exception(msg='Request timed out')
        raise

    if response.status_code != 200:
        raise Exception(f'Received status code: {response.status_code} from OSM service')

    bf = XMLData(dict_type=dict)
    return bf.data(fromstring(response.content))
    # return response.json()


def locations_to_bounding_box(latitude: float, longitude: float, padding: float = 0.01) -> List[float]:
    logger.debug(msg='Converting latitude and longitude to bounding box')
    bounding_box: list = [longitude - padding, latitude - padding, longitude + padding, latitude + padding]

    logger.debug(msg=f'Bounding box: {bounding_box}')
    return bounding_box


@lru_cache()
def fetch_osm_data(latitude: float, longitude: float) -> dict:
    if not latitude or not longitude:
        raise Exception('Missing latitude or longitude')

    logger.debug(msg='Fetching OSM data')
    bounding_box: List[float] = locations_to_bounding_box(latitude=latitude, longitude=longitude)
    nodes: dict = get_nodes(bounding_box=bounding_box)

    validate_osm_nodes(data=nodes)
    return nodes
