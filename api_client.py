import requests


class APIClient:
    def __init__(self, base_url):
        self.base_url = base_url.rstrip('/')

    def get(self, endpoint, **kwargs):
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        return requests.get(url, **kwargs)

    def post(self, endpoint, json=None, headers=None):
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        return requests.post(url, json=json, headers=headers)

    def put(self, endpoint, json=None, headers=None):
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        return requests.put(url, json=json, headers=headers)

    def delete(self, endpoint, **kwargs):
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        return requests.delete(url, **kwargs)
