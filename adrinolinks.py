from cloudscraper import CloudScraper as Session
from DrissionPage import ChromiumPage, ChromiumOptions
from proxyscrape import generate_random_ip
import os, time

def old_run_adrino_bot(link, proxy=None, headless=None):
    s=Session()
    # s.proxies=dict(http=proxy, https=proxy)
    r1=s.get(link, headers={'Referer': 'https://technicalzarir.blogspot.com', 'X-Forwarded-For': generate_random_ip()}, allow_redirects=False)
    print('Adrino Links:', r1.headers.get('Location'))
    
    
def run_adrino_bot(link, proxy=None, headless=None):
    # Avoid Proxy else CloudFlare will eat all data
    options = ChromiumOptions()
    options.add_extension(os.path.join(os.path.dirname(__file__), 'header_modifier'))
    options.add_extension(os.path.join(os.path.dirname(__file__), 'NopeCha'))
    options.auto_port()
    page = ChromiumPage(options)
    page.set.headers={'X-Forwarded-For': generate_random_ip()}
    # page.get('http://httpbin.org/headers')
    # time.sleep(50)
    page.get(link)
    attempt = 0
    while 1:
        time.sleep(3)
        if 'technicalzarir.blogspot.com' in page.url:
            break
        attempt+=1
        if attempt >= 13:
            page.quit()
            raise Exception('40 sec passed but cloudflare is still here.')
    
    print('Adrino Links:', page.url)
    page.quit()


if __name__=='__main__':
    from all_links import random_adrino
    run_adrino_bot(random_adrino, headless=False)


