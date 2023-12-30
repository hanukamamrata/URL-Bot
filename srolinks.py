from cloudscraper import CloudScraper as Session
from proxyscrape import generate_random_ip
from bs4 import BeautifulSoup
from time import sleep

def run_sro_bot(link, proxy=None, headless=None):
    s=Session()
    s.proxies=dict(http=proxy, https=proxy)
    r=s.get(link, headers={'Referer': 'https://technicalzarir.blogspot.com/'}, allow_redirects=False)
    s.cookies.set('ab', '2', domain='srolink.com')
    r=s.get(link, headers={'Referer': 'https://fastbdyt.com/'})
    doc = BeautifulSoup(r.text, 'html.parser')
    all_inputs = {i.get('name') : i.get('value') for i in doc.select('form input')}
    sleep(5)
    r=s.post('https://srolink.com/links/go', data=all_inputs, headers={'X-Requested-With': 'XMLHttpRequest'})

    print('Sro Links:', r.text)
    


if __name__=='__main__':
    from proxyscrape import get_session
    from all_links import random_srolinks
    print(random_srolinks)
    run_sro_bot(random_srolinks, get_session(), headless=False)


