import json
from consts import common_consts
from exceptions import finder_exceptions
from logging import getLogger


logger = getLogger(common_consts.LOGGER)


def contains_school_tag(tag):
    if not tag.get('k') or not tag.get('v'):
        logger.error(f'Missing tag key or value: {json.dumps(tag)}')
        raise Exception(finder_exceptions.MISSING_TAG_ATTRIBUTES)
    return tag['k'] == 'amenity' and tag['v'] == 'school'


def find_enrichment(data):
    logger.debug('Finding enrichment')
    enrichment = 0
    for entry in data:
        if 'tag' in entry:
            tags = entry['tag']
            if isinstance(tags, list):
                for t in tags:
                    if contains_school_tag(t):
                        enrichment += 1
                        break
            elif isinstance(tags, dict):
                if contains_school_tag(tags):
                    enrichment += 1
            else:
                logger.error(f'Expected tags list or dict, {type(tags)} given')
                raise Exception(finder_exceptions.UNKNOWN_TAG_STRUCTURE)
    logger.debug(f'Found enrichment: {enrichment}')
    return enrichment
