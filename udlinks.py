from time import sleep
from bs4 import BeautifulSoup
from cloudscraper import CloudScraper
from urllib.parse import urljoin, urlparse
from limiter import *
import re

class Session(CloudScraper):
    history = []
    def request(self, method, url, *a, **kw):
        self.history.append(url)
        kw['allow_redirects'] = False
        r = super().request(method, url, *a, **kw)
        loc = r.headers.get('Location')
        if not loc: return r
        return self.request(method, urljoin(url, loc), *a, **kw)

def get_req_data(link):
    s = Session()
    r = s.get(link, headers={'Referer': 'https://thekisscartoon.com/'})
    url = re.findall(r'url=(.*?)&', r.text)[0]
    r = s.get(url)
    while 1:
        d = BeautifulSoup(r.text, 'html.parser')
        f = d.select_one('form[name="tp"]')
        if not f: break
        r = s.post(f.get('action'), data={ i.get('name') : i.get('value') for i in f.select('input[name]')})
    referer = 'https://' + urlparse(s.history[-1]).netloc + '/'
    return referer

def run_udlinks_bot(link, proxy=None, headless=None):
    idn = 'urlbot-udlinks'
    if isCompleted(720, idn): return print('Target Completed. Function didn’t run.')
    ref = get_req_data(link)
    s = CloudScraper()
    s.cookies.set('ab', '2', domain='www.udlinks.com')
    s.proxies = dict(http=proxy, https=proxy)
    s.get(link, headers={'Referer': 'https://thekisscartoon.com/'}, stream=True)
    r = s.get(link, headers={'Referer': ref})
    d = BeautifulSoup(r.text, 'html.parser')
    data = { i.get('name') : i.get('value') for i in d.select('#go-link input[name]')}
    sleep(int(d.select_one('#timer').text))
    r = s.post('https://www.udlinks.com/links/go', headers={'X-Requested-With': 'XMLHttpRequest', 'Origin': 'https://www.udlinks.com', 'Referer': link}, data=data)
    if 'Go With earn' not in r.text: raise Exception('Error in UDLinks: %s' % r.text)
    print('UDLinks:', r.text)
    submitOne(idn)
    

if __name__=='__main__':
    from proxyscrape import get_session
    from all_links import random_udlinks
    print(random_udlinks)
    run_udlinks_bot(random_udlinks, get_session())


