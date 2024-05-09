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

def get_req_data(link, proxy=None):
    s = Session()
    s.proxies = dict(http=proxy, https=proxy)
    r = s.get(link, headers={'Referer': 'https://technicalzarir.blogspot.com/'})
    url = re.findall(r'url=(.*?)&', r.text)[0]
    r = s.get(url)
    while 1:
        # open('test.html', 'wb').write(r.content)
        d = BeautifulSoup(r.text, 'html.parser')
        f = d.select_one('#btn6, form#tp98')
        l = f.get('action', f.get('href'))
        for _ in range(2):
            if not l:
                f = f.parent
                l = f.get('action', f.get('href'))
        if not l: raise Exception('Referer Link is None')
        if 'malink.in' in l: break
        if f.get('action'):
            r = s.post(f.get('action'), data={ i.get('name') : i.get('value') for i in f.select('input[name]')})
        elif f.get('href'):
            r = s.get(f.get('href'), headers={'Referer': s.history[-1]})

    referer = 'https://' + urlparse(s.history[-1]).netloc + '/'
    return referer

def run_malink_bot(link, proxy=None, headless=None):
    # idn = 'urlbot-malink'
    # if isCompleted(720, idn): return print('Target Completed. Function did not run.')
    ref = get_req_data(link)
    s = CloudScraper()
    s.proxies = dict(http=proxy, https=proxy)
    s.cookies.set('ab', '2', domain='malink.in')
    s.get(link, headers={'Referer': 'https://technicalzarir.blogspot.com/'}, stream=True)
    r = s.get(link, headers={'Referer': ref})
    d = BeautifulSoup(r.text, 'html.parser')
    data = { i.get('name') : i.get('value') for i in d.select('#go-link input[name]')}
    sleep(int(d.select_one('#timer').text))
    r = s.post('https://malink.in/links/go', headers={'X-Requested-With': 'XMLHttpRequest', 'Origin': 'https://malink.in', 'Referer': link}, data=data)
    if 'Go With earn' not in r.text: raise Exception('Error in MaLink: %s' % r.text)
    print('MaLink:', r.text)
    # submitOne(idn)
    

if __name__=='__main__':
    from proxyscrape import get_session
    from all_links import random_malink
    print(random_malink)
    run_malink_bot(random_malink, get_session())


