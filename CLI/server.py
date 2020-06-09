from socket import *
from selenium import webdriver
import http.server
import socketserver
import threading


def create_server():
    port = 8000
    handler = http.server.SimpleHTTPRequestHandler
    httpd = socketserver.TCPServer(("", port), handler)
    print("serving at port:" + str(port))
    httpd.serve_forever()


threading.Thread(target=create_server).start()

print("Server has started. Continuing..")

browser = webdriver.Chrome()
browser.get("http://localhost:8000")

assert "<title>" in browser.page_source
