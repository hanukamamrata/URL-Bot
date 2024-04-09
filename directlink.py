from cloudscraper import CloudScraper
from urllib.parse import urljoin, urlparse
import re


class Session(CloudScraper):
    history = []
    def request(self, method, url, *a, **kw):
        self.history.append(url)
        kw['allow_redirects'] = False
        r = super().request(method, url, *a, **kw)
        loc = r.headers.get('Location')
        if loc:
            url = urljoin(self.history[-1], loc)
            return self.request(method, url, *a, **kw)
        return r


def run_directlink_bot(link, proxy=None, headless=False):
    s = Session()
    s.proxies=dict(http=proxy, https=proxy)
    r = s.get(link, headers={'Referer': 'https://www.facebook.com/'}, stream=True)
    for i in range(2):
        m = re.findall(r'replace\("(.*?)"\)', r.text)
        ref = f'https://{urlparse(s.history[-1]).netloc}/'
        try:
            r = s.get(m[0], headers={'Referer': ref}, stream=True)
        except IndexError:
            pass
        
    print('DirectLink:', True)
    # open('test.html','wb').write(r.content)


if __name__=='__main__':
    from proxyscrape import get_session
    from all_links import random_directlink
    print(random_directlink)
    run_directlink_bot(random_directlink, get_session())
