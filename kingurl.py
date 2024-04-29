from cloudscraper import CloudScraper as Session
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from cfbyass import cfbypass
from time import sleep
import re

def run_kingurl_bot(link, proxy=None, headless=False):
    ua, cookies = cfbypass('https://go.kingurl.in')
    s = Session()
    s.cookies = cookies
    s.headers = {'User-Agent': ua}
    s.proxies = dict(http=proxy, https=proxy)
    s.cookies.set('ab', '2', domain='kingurl.in')
    r = s.get(link, headers={'Referer': 'https://technicalzarir.blogspot.com/'})
    r = s.get(link.replace('://', '://go.'), headers={'Referer': 'https://a1.bankshiksha.in/'})
    doc = BeautifulSoup(r.text, 'html.parser')
    all_inputs = {i.get('name') : i.get('value') for i in doc.select('form input')}
    r=s.post('https://go.kingurl.in/links/go', data=all_inputs, headers={'X-Requested-With': 'XMLHttpRequest', 'Origin': 'https://go.kingurl.in', 'Referer': link.replace('://', '://go.')})
    if 'Error' in r.text:
        raise Exception('Error is King URL: Response:\n %s' % (r.text))
    print('King URL:', r.text)


if __name__ == '__main__':
    from proxyscrape import get_session
    from all_links import random_kingurl
    print(random_kingurl)
    run_kingurl_bot(random_kingurl, None, headless=False)
