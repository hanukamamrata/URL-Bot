from cloudscraper import CloudScraper as Session
from DrissionPage import ChromiumPage, ChromiumOptions
from proxyscrape import generate_random_ip
import os, time

def old_run_adrino_bot(link, proxy=None, headless=None):
    s=Session()
    # s.proxies=dict(http=proxy, https=proxy)
    r1=s.get(link, headers={'Referer': 'https://technicalzarir.blogspot.com', 'X-Forwarded-For': generate_random_ip()}, allow_redirects=False)
    loc = r1.headers.get('Location')
    if loc is None:
        raise Exception('Error in adrino links. Location is None')
    print('Adrino Links:', loc)
    
    
def run_adrino_bot(link, proxy=None, headless=None):
    # Avoid Proxy else CloudFlare will eat all data
    options = ChromiumOptions()
    #options.add_extension(os.path.join(os.path.dirname(__file__), 'header_modifier'))
    options.add_extension(os.path.join(os.path.dirname(__file__), 'NopeCha'))
    options.auto_port()
    page = ChromiumPage(options)
    page.get(link)
    attempt = 0
    while 1:
        time.sleep(3)
        if not 'Just a moment' in page.html:
            break
        attempt+=1
        if attempt >= 13:
            page.quit()
            raise Exception('40 sec passed but cloudflare is still here.')
    
    cookies = page.cookies
    ua = page.user_agent
    page.quit()
    
    s=Session()
    r1=s.get(link, headers={'User-Agent': ua, 'Referer': 'https://technicalzarir.blogspot.com', 'X-Forwarded-For': generate_random_ip()}, cookies=cookies, allow_redirects=False)
    loc = r1.headers.get('Location')
    if loc is None:
        raise Exception('Error in nano links. Location is None')
    print('Adrino Links:', loc)


if __name__=='__main__':
    from all_links import random_adrino
    run_adrino_bot(random_adrino, headless=False)


