import sys
from urllib.parse import urlparse

import requests
from requests_oauthlib import OAuth2Session
from selenium import webdriver
import os.path
import time
import http.server
import socketserver
from threading import Thread
from werkzeug.urls import url_decode

client_id = r'QeZPBSKqdvWFfBv1VYTSv9iFGz5T9pVJtNUjbEr6'
client_secret = r'0Wl3hAIGY9SvYOqTOLUiLNYa4OlCgZYdno9ZbcgCT7RGQ8x2f1l2HzZHsQ7ijC74A0mrOhhCVeZugqAmOADHIv5fHxaa7GqFNtQr11HX9ySTw3DscKsphCVi5P71mlGY'
redirect_uri = 'http://localhost:8000/'
token_url = 'https://ion.tjhsst.edu/oauth/token/'
scope = ["read"]


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
        print(open(".profile", "r").read())
    else:
        print(open(".profile", "r").read())

    while True:
        pass


def authenticate():
    oauth = OAuth2Session(client_id=client_id, redirect_uri=redirect_uri, scope=scope)
    authorization_url, state = oauth.authorization_url("https://ion.tjhsst.edu/oauth/authorize/")

    web_dir = os.path.join(os.path.dirname(__file__), 'oauth')
    os.chdir(web_dir)
    if os.path.exists("index.html"):
        os.remove("index.html")

    template = open("template.html", "r")
    index = open("index.html", "w")
    for line in template:
        index.write(line.replace('AUTH_URL', authorization_url))
    template.close()
    index.close()

    # server = Thread(target=create_server)
    # server.daemon = True
    # server.start()

    browser = webdriver.Chrome()
    browser.get("localhost:8000/")

    while "http://localhost:8000/?code" not in browser.current_url:
        http.server.
        time.sleep(0.25)

    url = browser.current_url
    gets = url_decode(url.replace("http://localhost:8000/?", ""))
    code = gets.get("code")
    if state == gets.get("state"):
        state = gets.get("state")
        print("states good")
    browser.quit()

    print(code)
    print(state)

    payload = {'grant_type': 'authorization_code', 'code': code, 'redirect_uri': redirect_uri, 'client_id': client_id,
               'client_secret': client_secret, 'csrfmiddlewaretoken': state}
    token = requests.post("https://ion.tjhsst.edu/oauth/token/", data=payload).json()
    print(token)
    headers = {'Authorization': f"Bearer {token['access_token']}"}

    # And finally get the user's profile!
    profile = requests.get("https://ion.tjhsst.edu/api/profile", headers=headers).json()
    print(profile)
    username = profile['ion_username']
    email = profile['tj_email']
    first_name = profile['first_name']
    last_name = profile['last_name']

    profileFile = open(".profile", "w")
    profileFile.write(profile)
    profileFile.close()

    # server.stop


def create_server():
    port = 8000
    handler = http.server.SimpleHTTPRequestHandler
    httpd = socketserver.TCPServer(("", port), handler)
    print("serving at port:" + str(port))
    httpd.serve_forever()

if __name__ == "__main__":
    main()
