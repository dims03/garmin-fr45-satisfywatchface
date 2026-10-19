import urllib.request
from html.parser import HTMLParser

class Links(HTMLParser):
    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            href = dict(attrs).get('href', '')
            if any(x in href.lower() for x in ('download', '.zip', 'sdkmanager')):
                print(href)

with urllib.request.urlopen('https://developer.garmin.com/connect-iq/sdk/', timeout=30) as r:
    Links().feed(r.read().decode())
