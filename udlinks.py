from cloudscraper import CloudScraper as Session
from proxyscrape import generate_random_ip
from bs4 import BeautifulSoup
from time import sleep

def run_udlinks_bot(link, proxy=None, headless=None):
    s=Session()
    s.proxies=dict(http=proxy, https=proxy)
    r=s.get(link, headers={'Referer': 'https://technicalzarir.blogspot.com/'}, allow_redirects=False)
    s.cookies.set('ab', '2', domain='www.udlinks.com')
    r=s.get(link, headers={'Referer': 'https://file.urbanpincode.com/'})
    doc = BeautifulSoup(r.text, 'html.parser')
    all_inputs = {i.get('name') : i.get('value') for i in doc.select('form input')}
    sleep(1)
    r=s.post('https://www.udlinks.com/links/go', data=all_inputs, headers={'X-Requested-With': 'XMLHttpRequest', 'Origin': 'https://www.udlinks.com', 'Referer': link})
    
    if 'Error' in r.text:
        raise Exception('Error is UDlinks Links: Response:\n %s\nCookie: %s' % (r.text, s.cookies))

    print('UDlinks Links:', r.text)
    


if __name__=='__main__':
    from proxyscrape import get_session
    from all_links import random_udlinks
    print(random_udlinks)
    run_udlinks_bot(random_udlinks, get_session(), headless=False)


