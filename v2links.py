from cloudscraper import CloudScraper
from bs4 import BeautifulSoup
from time import sleep
from random import random
from cfbyass import cfbypass
from urllib.parse import urlparse, urljoin
import re

class Session(CloudScraper):
    history = []
    def request(self, method, url, *args, **kwargs):
        self.history.append(url)
        kwargs['allow_redirects'] = False
        r = super().request(method, url, *args, **kwargs)
        loc = r.headers.get('Location')
        if loc:
            return self.request(method, urljoin(self.history[-1], loc), *args, **kwargs)
        return r

def isDuplicate():
    ip = Session().get('https://ip.oxylabs.io').text
    return ip in Session().get('https://ip-limiter-server.onrender.com/used').text

def addToDB():
    ip = Session().get('https://ip.oxylabs.io').text.replace('\n', '')
    return 'true' in Session().get('https://ip-limiter-server.onrender.com/add?ip=' + ip).text

def run_v2links_bot(link:str, proxy=None, headless=None):
    ua, cookies = cfbypass('https://v2links.me/')
    s=Session()
    s.cookies = cookies
    s.headers = {'User-Agent': ua}
    d = isDuplicate()
    if d: return print('V2Links Error: Duplicate View')
    s.cookies.set('ab', '2', domain='.v2links.me')
    r=s.get(link, headers={'Referer': 'https://thekisscartoon.com/'})
    apiUrl = re.findall(r"apiUrl\s*=\s*'(.*?)'", r.text)[0]
    s.get(apiUrl, params=dict(alias=link.split('/')[-1], random=str(random())), headers={'Referer': 'https://v2links.me/', 'Origin': 'https://v2links.me'})
    href = re.findall(r"href\s*=\s*'(.*?)'", r.text)[0]
    r = s.get(href, headers={'Referer': 'https://v2links.me/'})
    ref = f'https://{urlparse(s.history[-1]).netloc}/'
    r = s.get(link, headers={'Referer': ref})
    doc = BeautifulSoup(r.text, 'html.parser')
    all_inputs = {i.get('name') : i.get('value') for i in doc.select('form#go-link input[name]')}
    sleep(int(doc.select_one('#timer').text.strip()))
    r=s.post('https://v2links.me/links/go', data=all_inputs, headers={'X-Requested-With': 'XMLHttpRequest', 'Origin': 'https://v2links.me', 'Referer': link})
    
    if not d: addToDB()
    if 'Error' in r.text:
        raise Exception('Error in V2Links: Response:\n %s' % (r.text))
        
    print('V2Links:', r.text)
    


if __name__=='__main__':
    #from proxyscrape import get_session
    from all_links import random_v2links
    print(random_v2links)
    run_v2links_bot(random_v2links)


