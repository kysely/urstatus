from pprint import pprint
import requests

api_key = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxNzM3NDIsImV4cCI6MTUyODU4NTM1OSwidG9rZW5fdHlwZSI6ImFwaSJ9.LEU362ylP-4T8tYt39a6VJUuGDkFIvvUjttpHWxutiM'


def get_update(api_key=None):
    res = requests.get(
        'https://review-api.udacity.com/api/v1/me/submissions/completed/',
        headers={'Authorization': api_key},
        verify=False)

    return res.json()

c = get_update(api_key)

pprint(c)
