import requests
from consts import common_consts, osm_fetcher_consts
from exceptions import osm_fetcher_exceptions
from logging import getLogger
from lxml.etree import fromstring
from xmljson import XMLData


logger = getLogger(common_consts.LOGGER)


def get_nodes(bounding_box):
    logger.info('Getting OSM nodes')
    url = osm_fetcher_consts.BASE_URL.format(
        ','.join([str(x) for x in bounding_box]))
    logger.debug(f'OSM request: {url}')
    response = requests.get(url)

    if response.status_code != 200:
        logger.error(
            f'Got status code: {response.status_code} from osm request')
        return []

    bf = XMLData(dict_type=dict)
    return bf.data(fromstring(response.content))


def locations_to_bounding_box(latitude, longitude, padding=0.01):
    logger.debug('Converting latitude and longitude to bounding box')
    bounding_box = [None, None, None, None]
    bounding_box[0] = min(bounding_box[0] or longitude, longitude) - padding
    bounding_box[1] = min(bounding_box[1] or latitude, latitude) - padding
    bounding_box[2] = max(bounding_box[2] or longitude, longitude) + padding
    bounding_box[3] = max(bounding_box[3] or latitude, latitude) + padding
    logger.debug(f'Bounding box: {bounding_box}')
    return bounding_box


def fetch_osm_data(Latitude, Longitude, **_):
    logger.debug('Fetching OSM data')
    if not Latitude or not Longitude:
        logger.error('Missing latitude or longitude')
        raise Exception(osm_fetcher_exceptions.MISSING_FIELDS_ERROR)
    bb = locations_to_bounding_box(Latitude, Longitude)
    nodes = get_nodes(bb)
    return nodes
