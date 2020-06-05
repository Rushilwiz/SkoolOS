import sys
from urllib.parse import urlparse

import requests
from requests_oauthlib import OAuth2Session
from selenium import webdriver;
import os.path
import time

client_id = r'QeZPBSKqdvWFfBv1VYTSv9iFGz5T9pVJtNUjbEr6'
client_secret = r'0Wl3hAIGY9SvYOqTOLUiLNYa4OlCgZYdno9ZbcgCT7RGQ8x2f1l2HzZHsQ7ijC74A0mrOhhCVeZugqAmOADHIv5fHxaa7GqFNtQr11HX9ySTw3DscKsphCVi5P71mlGY'
redirect_uri = 'http://localhost:8000/'
token_url = 'https://ion.tjhsst.edu/oauth/token/'
scope=["read"]


def main():
    print("")
    print(" SSSSS   CCCCC  HH   HH  OOOOO   OOOOO  LL        OOOOO   SSSSS ")
    print("SS      CC    C HH   HH OO   OO OO   OO LL       OO   OO SS     ")
    print(" SSSSS  CC      HHHHHHH OO   OO OO   OO LL       OO   OO  SSSSS ")
    print("     SS CC    C HH   HH OO   OO OO   OO LL       OO   OO      SS")
    print(" SSSSS   CCCCC  HH   HH  OOOO0   OOOO0  LLLLLLL   OOOO0   SSSSS ")
    print("")

    if not os.path.exists(".profile"):
        authenticate()
    else:
        print(open(".profile", "r").read())



def authenticate():
    oauth = OAuth2Session(client_id=client_id, redirect_uri=redirect_uri, scope=scope)
    authorization_url, state = oauth.authorization_url("https://ion.tjhsst.edu/oauth/authorize/")
    browser = webdriver.Chrome()
    browser.get(authorization_url)

    while "http://localhost:8000/?code" not in browser.current_url:
        time.sleep(0.25)

    code = urlparse(browser.current_url).query[5:]
    browser.quit()

    payload = {'grant_type': 'authorization_code', 'code': code, 'redirect_uri': redirect_uri, 'client_id': client_id,
               'client_secret': client_secret, 'csrfmiddlewaretoken': state}
    token = requests.post("https://ion.tjhsst.edu/oauth/token/", data=payload).json()
    print(token)
    # headers = {'Authorization': f"Bearer {token['access_token']}"}
    #
    # # And finally get the user's profile!
    # profile = requests.get("https://ion.tjhsst.edu/api/profile", headers=headers).json()
    # username = profile['ion_username']
    # email = profile['tj_email']
    # first_name = profile['first_name']
    # last_name = profile['last_name']

    #print(profile)


if __name__ == "__main__":
    main()
