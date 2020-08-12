import json
from consts import common_consts
from logging import getLogger
from os import path


logger = getLogger(common_consts.LOGGER)


class Cacher:

    def __init__(self):
        self.cache = {}
        self.load_cache()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.store_cache()

    def load_cache(self):
        logger.debug('Loading cache')
        if path.exists(common_consts.CACHE):
            with open(common_consts.CACHE, 'r') as f:
                self.cache.update(json.load(f))
        else:
            self.cache = {}

    def store_cache(self):
        logger.debug('Storing cache')
        if self.cache:
            with open(common_consts.CACHE, 'w') as f:
                json.dump(self.cache, f)

    def search_cache(self, key):
        logger.debug(f'Searching cache for key {key}')
        return self.cache.get(key)

    def update_cache(self, entry):
        logger.debug(f'Updating cache with entry: {json.dumps(entry)}')
        self.cache.update(entry)
        self.store_cache()
