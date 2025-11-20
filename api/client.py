import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

BASE_URL = "https://gorest.co.in"
TOKEN = {"Authorization": f"Bearer e7861a22e7bd14084b161ae87e57b4fbbd3213d2ea92f5bfd14a4838fee76b7b"}

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

    # add thd access token to header
    if headers is None:
        headers = TOKEN.copy()
    else:
        headers.update(TOKEN)
    
    response = requests.request(
        method=method.upper(),
        url=url,
        headers=headers,
        json=json,
        params=params,
        verify=False            # turn off SSL verification
    )

    # FYI：这里，如果带有 expected_status 的情况下，会判断一下，但是这种情况下，caller如果也有assert，会卡在这里，那边其实就没有用了
    if expected_status is not None:
        assert response.status_code == expected_status, (
            f"Expected {expected_status}, got {response.status_code}. \n"
            f"Response Reason: {response.reason}. \n"
            f"Response Text: {response.text[:100]}. \n"
        )
    return response
