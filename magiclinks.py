from cloudscraper import CloudScraper as Session
from bs4 import BeautifulSoup
import re, time

def run_magic_bot(link, proxy=None, headless=None):
    s=Session()
    s.proxies=dict(http=proxy, https=proxy)
    s.cookies.set('ab', '2', domain='magiclink1.com')
    r0=s.get(link, headers={'Referer': 'https://technicalzarir.blogspot.com/'})
    r1=s.get(link, headers={'Referer': 'https://forextrading.govaf.com/'})
    doc=BeautifulSoup(r1.text, 'html.parser')
    form = doc.select_one('form')
    all_inputs = { k.get('name') : k.get('value') for k in form.select('input[value]')}
    time.sleep(2)
    r2 = s.post('https://magiclink1.com/links/go', data=all_inputs, headers={'X-Requested-With': 'XMLHttpRequest'})
    print('Magic Links:', r2.text)
    


if __name__=='__main__':
    from all_links import random_magic
    run_magic_bot(random_magic, headless=False)


