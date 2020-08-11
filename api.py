#!/usr/bin/env python3


import argparse
import json
import logging.handlers
import os
from consts import common_consts
from enricher import enrich_data
from exceptions import api_exceptions
from flask import Flask, Response, request


logging.basicConfig(filename=common_consts.LOGFILE,
                    format=common_consts.LOGGER_FORMAT,
                    level=logging.DEBUG)
logging.handlers.RotatingFileHandler(common_consts.LOGFILE, mode='a',
                                     maxBytes=common_consts.LOGFILE_SIZE,
                                     backupCount=2)
console_handler = logging.StreamHandler()
console_handler.setFormatter(logging.Formatter(common_consts.LOGGER_FORMAT))
console_handler.setLevel(logging.DEBUG)
logger = logging.getLogger(common_consts.LOGGER)
logger.addHandler(console_handler)

app = Flask(common_consts.APP_NAME)
logging.getLogger('werkzeug').addHandler(console_handler)


def validate_data():
    logger.debug('Validating data')
    if not request.is_json:
        return api_exceptions.CONTENT_TYPE_ERROR
    if not request.json:
        return api_exceptions.NO_DATA_ERROR
    if not isinstance(request.json, dict):
        return api_exceptions.DATA_JSON_ERROR
    d = request.json
    if not d.get('data') or not isinstance(d['data'], list):
        return api_exceptions.DATA_CONTENT_ERROR
    return None


@app.route('/api/enrich', methods=['POST'])
def enrich():
    logger.debug(f'Received request: {str(request)}')
    invalid = validate_data()
    if invalid:
        logger.warning(f'Received invalid data in request: {invalid}')
        return Response(invalid, status=400)
    try:
        logger.info('Attempting enrichment')
        enrich_data(request.json['data'])
        logger.debug(
            f'Successful enrichment, sending response: {request.json}')
        return Response(
            json.dumps(request.json), status=200, mimetype='application/json')
    except Exception as e:
        logger.error(f'Enrichment failed: {e}')
        return Response(str(e), status=400)


def parse_arguments():
    logger.debug('Parsing arguments')
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--debug', action='store_true', dest='debug',
                        help='Enable Flask debug mode')
    parser.add_argument('-e', '--env', default='development', dest='env',
                        help='Environment type')
    parser.add_argument('-o', '--host', dest='host', help='Server host')
    parser.add_argument('-p', '--port', dest='port', help='Server port')
    return vars(parser.parse_args())


def main():
    args = parse_arguments()
    if args.get('env', '') != 'production':
        os.environ['FLASK_ENV'] = args.pop('env')
    app.run(**args)


if __name__ == '__main__':
    main()
