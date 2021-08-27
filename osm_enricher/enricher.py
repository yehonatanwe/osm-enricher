import json
import logging
from multiprocessing.dummy import Pool as ThreadPool
from typing import List, Tuple

from osm_enricher.osm_fetcher import fetch_osm_data

logger: logging.Logger = logging.getLogger(name=__name__)


def get_enrichment_key(latitude: float, longitude: float) -> str:
    return f'{latitude}x{longitude}'


def update_data(data: List[dict], enrichments: dict) -> List[dict]:
    for entry in data:
        entry['SchoolCount'] = enrichments[get_enrichment_key(
            latitude=entry['Latitude'], longitude=entry['Longitude']
        )]
    return data


def contains_school_tag(tag: dict) -> bool:
    if not tag.get('k') or not tag.get('v'):
        raise Exception(f'Missing tag key or value: {json.dumps(tag)}')
    return tag['k'] == 'amenity' and tag['v'] == 'school'


def find_enrichment(data: list) -> int:
    logger.debug('Finding enrichment')
    enrichment: int = 0

    for entry in data:
        if tags := entry.get('tag'):
            if isinstance(tags, list):
                for tag in tags:
                    if contains_school_tag(tag=tag):
                        enrichment += 1
            elif isinstance(tags, dict):
                if contains_school_tag(tag=tags):
                    enrichment += 1
            else:
                raise Exception(f'Expected tags list or dict, instead found {type(tags)}')

    logger.debug(f'Found enrichment: {enrichment}')
    return enrichment


def validate_fields(item: dict) -> bool:
    return any(f not in item for f in ['Latitude', 'Longitude'])


def enrich_entry(entry: dict) -> Tuple[str, int]:
    logger.debug('Enriching entry')
    if validate_fields(item=entry):
        raise Exception('Entry is missing required fields')

    latitude: float = entry['Latitude']
    longitude: float = entry['Longitude']
    key: str = get_enrichment_key(latitude=latitude, longitude=longitude)
    logger.debug('Fetching OSM data')
    osm_data: dict = fetch_osm_data(latitude=latitude, longitude=longitude)

    logger.debug('Finding enrichment')
    enrichment: int = find_enrichment(data=osm_data['osm'].get('way', []))
    return key, enrichment


def enrich_data(data: List[dict]) -> List[dict]:
    if not data or not isinstance(data, list):
        raise Exception('Data is in invalid structure')

    logger.debug('Stating enrichment')
    with ThreadPool(processes=5) as pool:
        enrichments = pool.map(func=enrich_entry, iterable=data)

    logger.debug('Updating original data with enrichments')
    return update_data(data, dict(enrichments))
