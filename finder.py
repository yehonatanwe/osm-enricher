from consts import common_consts
from logging import getLogger


logger = getLogger(common_consts.LOGGER)


def contains_school_tag(k, v):
    return k == 'amenity' and v == 'school'


def find_enrichment(data):
    logger.debug('Finding enrichment')
    enrichment = 0
    for n in data['osm'].get('way', []):
        if 'tag' in n:
            tags = n['tag']
            if isinstance(tags, list):
                for t in tags:
                    if contains_school_tag(**t):
                        enrichment += 1
                        break
            elif isinstance(tags, dict):
                if contains_school_tag(**tags):
                    enrichment += 1
            else:
                logger.error(f'Expected tags list or dict, {type(tags)} given')
                raise Exception('Unknown tags structure')
    logger.debug(f'Found enrichment: {enrichment}')
    return enrichment
