import argparse
import logging
from typing import List, Tuple

import requests
from flask import Flask, jsonify, request

from osm_enricher.enricher import enrich_data

logging.basicConfig(level=logging.INFO)
logger: logging.Logger = logging.getLogger(name=__name__)

app: Flask = Flask(import_name=__name__)


def validate_request(data: dict) -> None:
    logger.info('Validating request data')
    assert data, 'Request data is empty'
    assert isinstance(data, dict), f'Expected data of type "dict", found {type(data)}'
    assert data.get('data'), 'Expected data to contain "data" key'


@app.post(rule='/api/enrich')
def enrich() -> Tuple[requests.Response, int]:
    logger.debug(msg=f'Received request: {str(request)}')

    data = getattr(request, 'json', None)
    try:
        validate_request(data=data)
    except AssertionError as e:
        logger.exception(msg='Bad request data')
        return jsonify({'error': str(e)}), 400

    try:
        logger.info(msg='Attempting enrichment')
        enriched_data: List[dict] = enrich_data(data=data.get('data'))
        logger.info(msg='Successful enrichment')
        logger.info(msg=f'Sending response: {enriched_data}')
        return jsonify(enriched_data), 200
    except Exception as e:
        logger.exception(msg='Enrichment failed')
        return jsonify({'error': str(e)}), 400


def parse_arguments() -> argparse.Namespace:
    logger.debug(msg='Parsing arguments')
    parser: argparse.ArgumentParser = argparse.ArgumentParser()
    parser.add_argument('-o', '--host', default='0.0.0.0', dest='host', help='Server host')
    parser.add_argument('-p', '--port', dest='port', help='Server port')
    return parser.parse_args()


def main(args: argparse.Namespace) -> None:
    app.run(host=args.host, port=args.port, )


if __name__ == '__main__':
    main(args=parse_arguments())
