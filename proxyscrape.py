from requests import get
from random import choices, randint, choice
from string import ascii_letters, digits
import requests

def get_session():
    countries = ['us', 'gb', 'au', 'ca', 'in', 'mx', 'nz']
    country = choice(countries) 
    st = ''.join(choices(ascii_letters+digits, k=randint(8,20)))
    #      http://73738zbpcibedc0-country-in-session-v0ntago2ly-lifetime-10:okjz6fk9nkkx3rc@rp.proxyscrape.com:6060
    pr = f'http://73738zbpcibedc0-country-{country}-session-{st}-lifetime-10:okjz6fk9nkkx3rc@rp.proxyscrape.com:6060'
    try:
        get('http://cloudflare.com', proxies=dict(http=pr,https=pr), timeout=10)
    except requests.exceptions.ReadTimeout:
        return get_session()
    return pr

if __name__ == '__main__':
    pr = get_session()
    print(pr)
    
    r=get('https://ip.oxylabs.io', proxies={'http':pr,'https':pr})
    print(r.text)
    
    
    