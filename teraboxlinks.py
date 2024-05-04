from cloudscraper import CloudScraper as Session
from proxyscrape import generate_random_ip
from limiter import *
import re

def run_terabox_bot(link, proxy=None, headless=None):
    idn = 'urlbot-terabox'
    if isCompleted(1428, idn): return print('Target Completed. Function did not run')
    s=Session()
    s.proxies=dict(http=proxy, https=proxy)
    r1=s.get(link, headers={'Referer': 'https://thekisscartoon.com/'}, allow_redirects=False, stream=True)
    loc = r1.headers.get('Location')
    if loc is None:
        raise Exception('Error in teraboxlinks links. Location is None')
    print('TeraBox Links:', loc)
    submitOne(idn)
    


if __name__=='__main__':
    from all_links import random_teraboxlinks
    from proxyscrape import get_session
    print(random_teraboxlinks)
    run_terabox_bot(random_teraboxlinks, get_session(), headless=False)


