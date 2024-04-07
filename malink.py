from cloudscraper import CloudScraper as Session
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from time import sleep

def run_malink_bot(link, proxy=None, headless=None):
    s=Session()
    s.proxies=dict(http=proxy, https=proxy)
    s.cookies.set('ab', '2', domain='malink.in')
    attempt = 0
    while attempt < 2:
        attempt += 1
        r=s.get(link, headers={'Referer': 'https://technicalzarir.blogspot.com/'}, allow_redirects=False)
        r=s.get(link, headers={'Referer': f'https://{urlparse(r.headers.get("Location")).netloc}/'})
        doc = BeautifulSoup(r.text, 'html.parser')
        all_inputs = {i.get('name') : i.get('value') for i in doc.select('form input')}
        if s.cookies.get('csrfToken'):
            break
        else: print('Retrying... Loop')
    sleep(3)
    r=s.post('https://malink.in/links/go', data=all_inputs, headers={'X-Requested-With': 'XMLHttpRequest', 'Origin': 'https://malink.in', 'Referer': link})
    
    if 'Error' in r.text:
        raise Exception('Error is MaLink: Response:\n %s' % (r.text))
    print('MaLink:', r.text)

if __name__=='__main__':
    from proxyscrape import get_session
    from all_links import random_malink
    print(random_malink)
    run_malink_bot(random_malink, get_session(), headless=False)


