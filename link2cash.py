from cloudscraper import CloudScraper as Session
from proxyscrape import generate_random_ip
from bs4 import BeautifulSoup
from time import sleep

def run_link2cash_bot(link, proxy=None, headless=None):
    s=Session()
    s.proxies=dict(http=proxy, https=proxy)
    attempt = 0
    while attempt < 2:
        attempt += 1
        r=s.get(link, headers={'Referer': 'https://technicalzarir.blogspot.com/'}, allow_redirects=False)
        s.cookies.set('ab', '2', domain='link2cash.in')
        r=s.get(link.replace('fly.', ''), headers={'Referer': 'https://sapnogalpo.online/'})
        doc = BeautifulSoup(r.text, 'html.parser')
        all_inputs = {i.get('name') : i.get('value') for i in doc.select('form input')}
        if s.cookies.get('csrfToken'):
            break
    sleep(10)
    r=s.post('https://link2cash.in/links/go', data=all_inputs, headers={'X-Requested-With': 'XMLHttpRequest', 'Origin': 'https://link2cash.in', 'Referer': link.replace('fly.', '')})
    
    if 'Error' in r.text:
        raise Exception('Error is Link2Cash: Response:\n %s\nCookie: %s' % (r.text, s.cookies))
    print('Link2Cash:', r.text)

if __name__=='__main__':
    from proxyscrape import get_session
    from all_links import random_link2cash
    print(random_link2cash)
    run_link2cash_bot(random_link2cash, get_session(), headless=False)


