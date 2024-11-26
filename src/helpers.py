import urllib.request
from src.ul_parser import ULParser

def fetch_html(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.9'
    }
    req = urllib.request.Request(url, headers=headers)

    with urllib.request.urlopen(req) as response:
        return response.read().decode('utf-8')

def find_ul_with_most_items(html):
    parser = ULParser()
    parser.feed(html)

    if not parser.result:
        return None

    extraced = extract_levels(parser.result)
    largest_ul = max(extraced, key=len)

    return len(largest_ul)

def extract_levels(data):
    if data is None:
        return []

    result = []
    current_level = []

    for item in data:
        if isinstance(item, list):
            result.extend(extract_levels(item))
        else:
            current_level.append(item)

    if current_level:
        result.insert(0, current_level)

    return result

