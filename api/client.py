import requests
from config.settings import BASE_URL

def send_request(method: str,
                 uri: str,
                 headers: dict = None,
                 body: dict = None,
                 params: dict = None,
                 expected_status: int = None):

    url = f"{BASE_URL}{uri}"
    
    response = requests.request(
        method=method.upper(),
        url=url,
        headers=headers,
        json=body,
        params=params
    )

    if expected_status is not None:
        assert response.status_code == expected_status, (
            f"Expected {expected_status}, got {response.status_code}. "
            f"Response: {response.text}"
        )
    return response
