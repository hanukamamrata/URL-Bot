from cloudscraper import CloudScraper as Session
from bs4 import BeautifulSoup
from time import sleep
from urllib.parse import urlparse
import re, ssl
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def isDuplicate():
    ip = Session().get('https://ip.oxylabs.io').text
    return ip in Session().get('https://ip-limiter-server.onrender.com/used').text

def addToDB():
    ip = Session().get('https://ip.oxylabs.io').text.replace('\n', '')
    return 'true' in Session().get('https://ip-limiter-server.onrender.com/add?ip=' + ip).text

def run_telegram_bot(link, proxy=None, headless=None):
    s=Session(ssl_context=ssl._create_unverified_context())
    d = isDuplicate()
    if d:
        from proxy_server import working_proxy as k
        s.proxies=dict(http=k, https=k)
    s.cookies.set('ab', '2', domain='telegramlink.in')
    r=s.get(link, headers={'Referer': 'https://www.pcgamespunch.com/'}, verify=False)
    open('test.html','wb').write(r.content)
    url = re.findall(r'href\s*=\s*"(.*?)"', r.text)[0]
    r=s.get(url, verify=False)
    doc = BeautifulSoup(r.text, 'html.parser')
    url = doc.select_one('form[name="tp"]').get('action')
    r=s.post(url, data={'tp2': link.split('/')[-1]}, verify=False)
    doc = BeautifulSoup(r.text, 'html.parser')
    url = doc.select_one('#btn6').get('href')
    r=s.get(url, verify=False)
    url = re.findall(r'href\s*=\s*"(.*?)"', r.text)[0]
    r=s.get(url, verify=False)
    doc = BeautifulSoup(r.text, 'html.parser')
    url = doc.select_one('#btn6').get('href')
    ref = f'https://{urlparse(url).netloc}/'
    r = s.get(link, headers={'Referer': ref}, verify=False)
    doc = BeautifulSoup(r.text, 'html.parser')
    all_inputs = {i.get('name') : i.get('value') for i in doc.select('form#go-link input[name]')}
    sleep(1)
    r=s.post('https://telegramlink.in/links/go', data=all_inputs, headers={'X-Requested-With': 'XMLHttpRequest', 'Origin': 'https://telegramlink.in', 'Referer': link}, verify=False)
    
    if not d: addToDB()
    if 'Error' in r.text:
        raise Exception('Error is Telegram Links: Response:\n %s' % (r.text))
        
    print('Telegram Links:', r.text)
    


if __name__=='__main__':
    #from proxyscrape import get_session
    from all_links import random_telegramlinks
    print(random_telegramlinks)
    run_telegram_bot(random_telegramlinks)


