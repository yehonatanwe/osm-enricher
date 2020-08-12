#!/usr/bin/env python3


import argparse
import requests


DATA = {"data": [
    {"Suburb": "Footscray", "Rooms": 3, "Date": "2016-03-12", "Postcode": 3011,
     "Bedroom2": 3, "Bathroom": 1, "Car": 1, "Landsize": 292,
     "YearBuilt": 1900, "Latitude": -37.797, "Longitude": 144.9051,
     "Address": "9 LynchSt 3011, Melbourne, Australia"}]}


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--data', dest='data', default=DATA)
    parser.add_argument('-o', '--host', dest='host', default='127.0.0.1')
    parser.add_argument('-p', '--port', dest='port', default=5000)
    return vars(parser.parse_args())


def main():
    args = parse_arguments()
    response = requests.post(url='http://{host}:{port}/api/enrich'.format(
        **args), json=args['data'])
    print(response.content.decode('utf-8'))


if __name__ == '__main__':
    main()
