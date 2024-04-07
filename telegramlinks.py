from cloudscraper import CloudScraper as Session
from bs4 import BeautifulSoup
from time import sleep
from urllib.parse import urlparse
import re

def run_telegram_bot(link, proxy=None, headless=None):
    s=Session()
    # s.proxies=dict(http=proxy, https=proxy)
    s.cookies.set('ab', '2', domain='telegramlink.in')
    r=s.get(link, headers={'Referer': 'https://www.pcgamespunch.com/'})
    url = re.findall(r'href\s*=\s*"(.*?)"', r.text)[0]
    r=s.get(url)
    doc = BeautifulSoup(r.text, 'html.parser')
    url = doc.select_one('form[name="tp"]').get('action')
    r=s.post(url, data={'tp2': link.split('/')[-1]})
    doc = BeautifulSoup(r.text, 'html.parser')
    url = doc.select_one('#btn6').get('href')
    r=s.get(url)
    url = re.findall(r'href\s*=\s*"(.*?)"', r.text)[0]
    r=s.get(url)
    doc = BeautifulSoup(r.text, 'html.parser')
    url = doc.select_one('#btn6').get('href')
    ref = f'https://{urlparse(url).netloc}/'
    r = s.get(link, headers={'Referer': ref})
    doc = BeautifulSoup(r.text, 'html.parser')
    all_inputs = {i.get('name') : i.get('value') for i in doc.select('form#go-link input[name]')}
    sleep(1)
    r=s.post('https://telegramlink.in/links/go', data=all_inputs, headers={'X-Requested-With': 'XMLHttpRequest', 'Origin': 'https://telegramlink.in', 'Referer': link})
    
    if 'Error' in r.text:
        raise Exception('Error is Telegram Links: Response:\n %s' % (r.text))
        
    print('Telegram Links:', r.text)
    


if __name__=='__main__':
    from proxyscrape import get_session
    from all_links import random_telegramlinks
    print(random_telegramlinks)
    run_telegram_bot(random_telegramlinks)


