import requests
import urllib3
from config.consts import BASE_URL

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

'''
在这里，path需要包含 path parameter，而 query parameters需要以 dict 格式放在 params 参数中。
如果需要login的情况下，如果使用的是token认证，token要带在 headers 参数中传入。
'''
def send_request(method: str,
                 path: str,
                 headers: dict = None,
                 json: dict = None,
                 params: dict = None,
                 expected_status: int = None):

    url = f"{BASE_URL}{path}"
    
    response = requests.request(
        method=method.upper(),
        url=url,
        headers=headers,
        json=json,
        params=params,
        verify=False            # turn off SSL verification
    )

    if expected_status is not None:
        assert response.status_code == expected_status, (
            f"Expected {expected_status}, got {response.status_code}. \n"
            f"Response Reason: {response.reason}. \n"
            f"Response Text: {response.text[:100]}. \n"
        )
    return response
