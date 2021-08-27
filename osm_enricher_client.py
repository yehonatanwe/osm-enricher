#!/usr/bin/env python3


import argparse
import json

import requests

DATA: dict = {
    'data': [
        {
            'Suburb': 'Footscray',
            'Rooms': 3,
            'Date': '2016-03-12',
            'Postcode': 3011,
            'Bedroom2': 3,
            'Bathroom': 1,
            'Car': 1,
            'Landsize': 292,
            'YearBuilt': 1900,
            'Latitude': -37.797,
            'Longitude': 144.9051,
            'Address': '9 LynchSt 3011, Melbourne, Australia'
        }
    ]
}


def parse_arguments() -> argparse.Namespace:
    parser: argparse.ArgumentParser = argparse.ArgumentParser()
    parser.add_argument('-d', '--data', dest='data', default=DATA)
    parser.add_argument('-o', '--host', dest='host', default='127.0.0.1')
    parser.add_argument('-p', '--port', dest='port', default=5000)
    return parser.parse_args()


def main(args: argparse.Namespace) -> None:
    response: requests.Response = requests.post(
        url=f'http://{args.host}:{args.port}/api/enrich',
        headers={'Content-Type': 'Application/json'},
        json=args.data)

    if response.status_code != 200:
        raise Exception(response.reason)

    print(json.dumps(response.json(), indent=2))


if __name__ == '__main__':
    main(args=parse_arguments())
