from tldextract import extract
from requests import get

all_list_txt = get('https://filters.adtidy.org/extension/chromium/filters/15.txt').text

def is_ads(url):
    if 'technicalzarir.blogspot.com' in url or 'www.google.com/url?sa' in url:
        return False
    ex = extract(url)
    domain = ex.domain + '.' + ex.suffix
    return domain in all_list_txt

