import sys
from src.helpers import fetch_html, find_ul_with_most_items

def main():
    if len(sys.argv) != 2:
        print("Provide url with HTML content -> python main.py https://some-website.com")
        sys.exit(1)

    url = sys.argv[1]
    raw_html = fetch_html(url)

    children_amount = find_ul_with_most_items(raw_html)

    if children_amount == 0 or children_amount == None:
        print("No unordered list found")
    else:
        print(f"The unordered list with the most direct children contains {children_amount} items.")

if __name__ == '__main__':
    main()
