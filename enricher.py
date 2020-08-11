from cacher import Cacher
from consts import common_consts, enricher_consts
from exceptions import enricher_exceptions
from logging import getLogger
from multiprocessing.dummy import Pool as ThreadPool
from osm_fetcher import fetch_osm_data
from finder import find_enrichment


logger = getLogger(common_consts.LOGGER)
cache = Cacher()


def get_enrichment_key(Latitude, Longitude, **_):
    return f'{Latitude}{enricher_consts.DELIMITER}{Longitude}'


def update_data(data, enrichment):
    for e in data:
        e['School Count'] = enrichment[get_enrichment_key(**e)]


def validate_fields(item):
    return any(k not in item for k in enricher_consts.REQUIRED_FIELDS)


def enrich_entry(entry):
    logger.debug('Enriching entry')
    if validate_fields(entry):
        logger.error('Entry is missing required fields')
        raise Exception(enricher_exceptions.MISSING_DATA_ERROR)
    key = get_enrichment_key(**entry)
    enrichment = cache.search_cache(key)
    if enrichment is not None:
        logger.info('Enrichment found in cache')
    else:
        logger.debug('Fetching OSM data')
        osm_data = fetch_osm_data(**entry)
        logger.debug('Finding enrichment')
        enrichment = find_enrichment(osm_data)
        logger.debug('Updating cache')
        cache.update_cache({key: enrichment})
    return key, enrichment


def enrich_data(data):
    logger.debug('Stating enrichment for data')
    if not data or not isinstance(data, list):
        logger.error('Provided data is in invalid structure')
        raise Exception(enricher_exceptions.MISSING_DATA_ERROR)
    with ThreadPool(enricher_consts.POOL_SIZE) as pool:
        enriched_data = pool.map(enrich_entry, data)
    logger.debug('Updating original data with enrichment')
    update_data(data, dict(enriched_data))
