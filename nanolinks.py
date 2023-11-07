from cloudscraper import CloudScraper as Session
import re

def run_nano_bot(link, proxy=None, headless=None):
    s=Session()
    s.proxies=dict(http=proxy, https=proxy)
    r1=s.get(link, headers={'Referer': 'https://technicalzarir.blogspot.com'}, allow_redirects=False)
    print('Nano Links:', r1.headers.get('Location'))
    


if __name__=='__main__':
    from all_links import random_nanolinks
    run_nano_bot(random_nanolinks, headless=False)


