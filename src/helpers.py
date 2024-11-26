import urllib.request
def fetch_html(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.9'
    }
    req = urllib.request.Request(url, headers=headers)

    with urllib.request.urlopen(req) as response:
        return response.read().decode('utf-8')