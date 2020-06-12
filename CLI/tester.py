import requests
import webbrowser

URL = "chrome://version"
webbrowser.open_new_tab(URL)
r = requests.get(URL)
print(r.json())