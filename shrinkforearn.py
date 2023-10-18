from time import sleep
from requests import Session
from bs4 import BeautifulSoup

def run_shrinkforearn_bot(link:str, proxy=None, headless=None):
    base_domain = 'shrinkforearn.xyz'
    replace_with = 'shrinkforearn.in'
    org_refer = 'https://technicalzarir.blogspot.com'
    refer_link = 'https://wp.uploadfiles.in'
    s=Session()
    if proxy:
        s.proxies={'http':proxy,'https':proxy}
    s.cookies.set('ab','2', domain=replace_with.split('/')[0])
    ua='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36'
    hl=link
    while hl:
        hl=s.get(hl, headers={'Referer': org_refer, 'User-Agent': ua}, allow_redirects=False).headers.get('Location')
        
    r1=s.get(link.replace(base_domain, replace_with), headers={'User-Agent': ua, 'Referer': refer_link})
    html=r1.text
    soap=BeautifulSoup(html, 'html.parser')
    form_inputs = soap.select('form input')
    input_dict = {}
    for elem in form_inputs:
        input_dict[elem.get('name')] = elem.get('value')
    try:
        sleep(int(soap.select_one('#timer').text.strip()))
    except:
        import traceback
        print(traceback.format_exc(), '\n\n', html)
    r2=s.post(f'https://{replace_with}/links/go', data=input_dict, headers={'User-Agent': ua, 'X-Requested-With': 'XMLHttpRequest'})
    try:
        json=r2.json()
    except:
        raise Exception(r2.text)
    if not json.get('status')=='success':
        raise Exception(r2.text)
    else:
        print('Shrink For Earn:',json)

if __name__ == "__main__":
    from all_links import random_shrinkforearn
    run_shrinkforearn_bot(random_shrinkforearn, headless=False)
    