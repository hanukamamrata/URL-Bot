import requests, asyncio, aiohttp
from aiohttp_proxy import ProxyConnector
from bs4 import BeautifulSoup
import re

async def check_proxy(proxy_url):
    url = 'http://ip.oxylabs.com'
    scode = 200
    contains = '.'
    
    connector = ProxyConnector.from_url(proxy_url, limit=50000)
    try:
        async with aiohttp.ClientSession(connector=connector) as session:
            async with session.get(url, timeout=10) as response:
                if response.status == scode and contains in await response.text():
                    return True
                else:
                    return False
    except Exception as detail:
        return False

async def check_and_send_proxy(proxy):
    prot, addr = proxy.split('://')
    ip, port = addr.split(':')
    if ip not in used_ip:
        is_working = await check_proxy(proxy)
        if is_working:
            return proxy
    return None

async def find_working_proxy(proxy_txt):
    proxies = proxy_txt.strip().split('\n')
    print('Total proxies:', len(proxies), flush=True)
    tasks = [check_and_send_proxy(reformat_proxy(proxy)) for proxy in proxies]
    for task in asyncio.as_completed(tasks):
        working_proxy = await task
        if working_proxy:
            return working_proxy

    return None

def reformat_proxy(pr):
    if not pr: return pr
    prot, addr = pr.split('://')
    host, port = addr.split(':')
    a,b,c,d = host.split('.')
    a,b,c,d = int(a), int(b), int(c), int(d)
    port = int(port)
    ip = prot + '://' + '.'.join([str(a), str(b), str(c), str(d)]) + ':' + str(port)
    return ip

def add_to_db(proxy):
    if not proxy: return None
    prot, addr = proxy.split('://')
    ip, port = addr.split(':')
    r = requests.get(f'https://ip-limiter-server.onrender.com/add?ip={ip}')
    return r.text == 'true'
    
def remove_from_db(proxy):
    if not proxy: return None
    prot, addr = proxy.split('://')
    ip, port = addr.split(':')
    r = requests.get(f'https://ip-limiter-server.onrender.com/del?ip={ip}')
    return r.text == 'true'

def give_them_prot(proxies, nm='http'):
    proxy_list = proxies.strip().split('\n')
    new_pr = [f'{nm}://{pr}' for pr in proxy_list]
    return '\n'.join(new_pr) + '\n'

def get_all_proxies(sr:dict):
    all_pr=''
    for key, value in sr.items():
        for url in value:
            all_pr += give_them_prot(requests.get(url).text, key)
    return all_pr

def geonode_proxies():
    all_pr = ''
    countries = []
    ct = '&'.join(['country=' + i for i in countries])
    try:
        for i in range(1,3):
            resp = requests.get(f'https://proxylist.geonode.com/api/proxy-list?limit=500&page={i}&sort_by=lastChecked&sort_type=desc&'+ct, headers={'Origin': 'https://geonode.com'})
            data = resp.json()['data']
            for item in data:
                for prt in item['protocols']:
                    pr = prt + '://' + item['ip'] + ':' + item['port']
                    all_pr += pr + '\n'
    except:
        import traceback
        print(traceback.format_exc())
    return all_pr

def fpl_proxies():
    resp = requests.get('https://free-proxy-list.net/')
    soap = BeautifulSoup(resp.text, 'html.parser')
    ta = soap.select_one('textarea')
    ta_text = ta.text.split('\n')[3:]
    return give_them_prot('\n'.join(ta_text))

def psProxies():
    r = requests.get('https://api.proxyscrape.com/v3/free-proxy-list/get?request=displayproxies&proxy_format=protocolipport&format=text')
    pl = r.text.replace('\r\n','\n')
    return pl

api_dict = {
    'http': [],
    'socks4': [],
    'socks5': []
}

all_resp_text = ''
all_resp_text += get_all_proxies(api_dict)
all_resp_text += geonode_proxies()
all_resp_text += fpl_proxies()
all_resp_text += psProxies()

used_ip = requests.get('https://ip-limiter-server.onrender.com/used').text

working_proxy = asyncio.run(find_working_proxy(all_resp_text))

commit_used = lambda x=working_proxy: add_to_db(x)
discommit_used = lambda x=working_proxy: remove_from_db(x)

commit_used()

print(working_proxy, flush=True)
