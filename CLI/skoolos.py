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
import pprint
from PyInquirer import prompt, print_json
import json
import os
import argparse
from cryptography.fernet import Fernet

client_id = r'QeZPBSKqdvWFfBv1VYTSv9iFGz5T9pVJtNUjbEr6'
client_secret = r'0Wl3hAIGY9SvYOqTOLUiLNYa4OlCgZYdno9ZbcgCT7RGQ8x2f1l2HzZHsQ7ijC74A0mrOhhCVeZugqAmOADHIv5fHxaa7GqFNtQr11HX9ySTw3DscKsphCVi5P71mlGY'
redirect_uri = 'http://localhost:8000/'
token_url = 'https://ion.tjhsst.edu/oauth/token/'
scope = ["read"]


def main():
    print("")
    print("░██████╗██╗░░██╗░█████╗░░█████╗░██╗░░░░░  ░█████╗░░██████╗")
    print("██╔════╝██║░██╔╝██╔══██╗██╔══██╗██║░░░░░  ██╔══██╗██╔════╝")
    print("╚█████╗░█████═╝░██║░░██║██║░░██║██║░░░░░  ██║░░██║╚█████╗░")
    print("░╚═══██╗██╔═██╗░██║░░██║██║░░██║██║░░░░░  ██║░░██║░╚═══██╗")
    print("██████╔╝██║░╚██╗╚█████╔╝╚█████╔╝███████╗  ╚█████╔╝██████╔╝")
    print("╚═════╝░╚═╝░░╚═╝░╚════╝░░╚════╝░╚══════╝  ░╚════╝░╚═════╝░")
    print("")

    if not os.path.exists(".profile"):
        input("Welcome to SkoolOS. Press any key to create an account")
        authenticate()
    else:
        print(open(".profile", "r").read())

    # while True:
    #     pass

def authenticate():
    oauth = OAuth2Session(client_id=client_id, redirect_uri=redirect_uri, scope=scope)
    authorization_url, state = oauth.authorization_url("https://ion.tjhsst.edu/oauth/authorize/")

    cdir = os.getcwd()
    #Linux: chromdriver-linux
    #Macos: chromdriver-mac
    #Windows: chromdriver.exe
    path = os.path.join(cdir, "chromedriver-mac")
    print(path)
    browser = webdriver.Chrome(path)
    #browser = webdriver.Safari()

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

    server = Thread(target=create_server)
    server.daemon = True
    server.start()

    browser.get("localhost:8000/")
    print(1)
    while "localhost:8000/callback/?code" not in browser.current_url:
        time.sleep(0.25)

    url = browser.current_url
    gets = url_decode(url.replace("localhost:8000/callback/?", ""))
    code = gets.get("code")
    print(2)
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
    
    pprint.pprint(profile)
    username = profile['ion_username']
    email = profile['tj_email']
    first_name = profile['first_name']
    last_name = profile['last_name']

    os.chdir(cdir)
    profileFile = open(".profile", "w")
    #profileFile.write(profile.text())
    key = Fernet.generate_key()
    file = open('key.key', 'wb')
    file.write(key) # The key is type bytes still
    file.close()
    profileFile.write(str(profile))
    profileFile.close()

    sys.exit


def create_server():
    port = 8000
    handler = http.server.SimpleHTTPRequestHandler
    httpd = socketserver.TCPServer(("", port), handler)
    print("serving at port:" + str(port))
    httpd.serve_forever()

if __name__ == "__main__":
    main()
