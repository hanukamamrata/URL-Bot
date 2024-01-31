from cloudscraper import CloudScraper as Session
from proxyscrape import generate_random_ip
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from time import sleep

def run_zagl_bot(link, proxy=None, headless=None):
    s=Session()
    s.cookies.set('ab', '2', domain='za.gl')
    r = s.get(link, headers={'Referer':'https://technicalzarir.blogspot.com/'})
    doc = BeautifulSoup(r.text, 'html.parser')
    all_inputs = {i.get('name') : i.get('value') for i in doc.select('form input')}
    all_inputs['givenX'] = 'R/5bGA2cx1NFHZN0FfUEPQ=='
    all_inputs['givenY'] = '8kBjUf4B/6WDRv3eeMFBvA=='
    all_inputs['X'] = '185'
    all_inputs['Y'] = '248'
    s.proxies=dict(http=proxy, https=proxy)
    r = s.post(link, data=all_inputs, headers={'Referer': link, 'Origin': 'https://za.gl'}, allow_redirects=False, stream=True)
    
    loc = r.headers.get('Location')
    if 'session' not in loc:
        raise Exception('Captcha is not passed')
    token = loc.split('?session=')[-1]
    sleep(10)
    r = s.post('https://za.gl/links/go', data={'ad_form_data': token})
    print(r.text)
    


if __name__=='__main__':
    from proxyscrape import get_session
    from all_links import random_zagl
    print(random_zagl)
    run_zagl_bot(random_zagl, get_session(), headless=False)


