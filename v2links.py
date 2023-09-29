from time import sleep
from requests import Session
from bs4 import BeautifulSoup
from proxyscrape import get_session

def run_v2links_bot(link:str, proxy=None, headless=True):
    s=Session()
    if proxy:
        #proxy = get_session()
        s.proxies={'http':proxy,'https':proxy}
    s.cookies.set('ab','2', domain='.vzu.us')
    ua='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36'
    r1=s.get(link.replace('vlshort.com', 'vzu.us'), headers={'User-Agent': ua, 'Referer': 'https://www.sahityt.com'})
    html=r1.text
    soap=BeautifulSoup(html, 'html.parser')
    form_inputs = soap.select('form#go-link input')
    input_dict = {}
    for elem in form_inputs:
        input_dict[elem.get('name')] = elem.get('value')
    try:
        sleep(int(soap.select_one('#timer').text.strip()))
    except:
        import traceback
        print(traceback.format_exc(), '\n\n', html)
    r2=s.post('https://vzu.us/links/go', data=input_dict, headers={'User-Agent': ua, 'X-Requested-With': 'XMLHttpRequest'})
    try:
        json=r2.json()
    except:
        raise Exception(r2.text)
    if not json.get('status')=='success':
        raise Exception(r2.text)
    else:
        print('V2links:',json)

if __name__ == "__main__":
    from all_links import random_v2links
    run_v2links_bot(random_v2links, proxy=False, headless=False)

