from cloudscraper import CloudScraper as Session
import re

def run_directlink_bot(link, proxy=None, headless=None):
    s=Session()
    s.proxies=dict(http=proxy, https=proxy)
    r1=s.get(link, headers={'Referer': 'https://facebook.com'})
    match = re.findall(r'name="token" value="(.*?)"', r1.text)
    if not match:
        if 'Anonymous Proxy detected' in r1.text:
            raise Exception('Request Blocked because proxy detected.')
        raise Exception('Error: No token found.')
    
    token=match[0]
    r2=s.get(f'https://www.toprevenuegate.com/api/users', params={'token': token, 'uuid':'', 'pii':'', 'in': 'false'}, headers={'Referer': link}, allow_redirects=False)
    print(r2.headers.get('Location'))
    


if __name__=='__main__':
    from all_links import random_directlink
    run_directlink_bot(random_directlink, headless=False)


