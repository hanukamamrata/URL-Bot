from time import sleep
from requests import Session
from bs4 import BeautifulSoup

def run_e2share_bot(link:str, proxy=None, headless=True):
    s=Session()
    if proxy:
        s.proxies={'http':proxy,'https':proxy}
    s.cookies.set('ab','2', domain='.insurance.techyinfo.in')
    ua='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36'
    r1=s.get(link.replace('e2share.in', 'insurance.techyinfo.in'), headers={'User-Agent': ua, 'Referer': 'https://loan.techyinfo.in'})
    html=r1.text
    soap=BeautifulSoup(html, 'html.parser')
    form_inputs = soap.select('form input')
    input_dict = {}
    for elem in form_inputs:
        input_dict[elem.get('name')] = elem.get('value')
    sleep(int(soap.select_one('#timer').text.strip()))
    r2=s.post('https://insurance.techyinfo.in/links/go', data=input_dict, headers={'User-Agent': ua, 'X-Requested-With': 'XMLHttpRequest'})
    try:
        json=r2.json()
    except:
        raise Exception(r2.text)
    if not json.get('status')=='success':
        raise Exception(r2.text)
    else:
        print('E2Share:',json)

if __name__ == "__main__":
    from all_links import random_e2share
    run_e2share_bot(random_e2share, headless=False)

