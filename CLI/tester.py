import requests
import webbrowser

URL = "chrome://version"
webbrowser.open_new_tab(URL)
r = requests.get(url = URL)
print(r.json())