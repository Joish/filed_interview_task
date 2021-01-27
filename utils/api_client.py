import json
class ApiClient:
    """Performs API requests."""

    def __init__(self, app):
        self.client = app.test_client()

    def get(self, url, **kwargs):
        """Sends GET request and returns the response."""
        return self.client.get(url, headers=self.request_headers(), **kwargs)

    def post(self, url, data, **kwargs):
        """Sends GET request and returns the response."""
        return self.client.post(url, headers=self.request_headers(),json=data, **kwargs)

    def request_headers(self):
        return {
            "Content-Type": 'application/json'
        }
