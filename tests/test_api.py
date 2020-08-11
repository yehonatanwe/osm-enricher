from api import
import requests

url = 'http://localhost:5000/api/enrich'


def test_enrich():
    api.main()
    r = requests.get(url=url)
    assert r.status_code is 400


# class TestApi:
#
#     def __init__(self):
#         api.main()
    #
    # def test_enrich(self):
