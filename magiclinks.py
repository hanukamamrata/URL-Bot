from cloudscraper import CloudScraper as Session
import re

def run_magic_bot(link, proxy=None, headless=None):
    s=Session()
    s.proxies=dict(http=proxy, https=proxy)
    r1=s.get(link, headers={'Referer': 'https://forextrading.govaf.com/'})
    open('test.html', 'w').write(r1.text)
    


if __name__=='__main__':
    from all_links import random_magic
    print(random_magic)
    run_magic_bot(random_magic, headless=False)


