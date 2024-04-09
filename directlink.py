from cloudscraper import CloudScraper as Session

def run_directlink_bot(link, proxy=None, headless=False):
    s = Session()
    s.proxies=dict(http=proxy, https=proxy)
    r = s.get(link, headers={'Referer': 'https://www.facebook.com/'}, stream=True)
    open('test.html','wb').write(r.content)


if __name__=='__main__':
    from proxyscrape import get_session
    from all_links import random_directlink
    print(random_directlink)
    run_directlink_bot(random_directlink, get_session())
