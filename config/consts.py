import os

BASE_URL = "https://gorest.co.in"
HEADERS = {"Authorization": f"Bearer e7861a22e7bd14084b161ae87e57b4fbbd3213d2ea92f5bfd14a4838fee76b7b"}

CURR_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(CURR_DIR)
USER_FILE_PATH = os.path.join(ROOT_DIR, "user_info.json")
POST_FILE_PATH = os.path.join(ROOT_DIR, "post_info.json")
COMMENT_FILE_PATH = os.path.join(ROOT_DIR, "comment_info.json")