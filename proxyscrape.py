from requests import get
from random import choices, randint, choice
from string import ascii_letters, digits
import requests, random

def get_session():
    countries = ['us', 'gb', 'au', 'ca', 'in', 'mx', 'nz']
    country = choice(countries) 
    st = ''.join(choices(ascii_letters+digits, k=randint(8,20)))
    pr = f'http://ieyqmoirvvpfdh6-country-{country}-session-{st}-lifetime-10:7dvv9jwswj601ad@rp.proxyscrape.com:6060'
    #try:
    #    get('http://google.com', proxies=dict(http=pr,https=pr), timeout=10)
    #except requests.exceptions.ReadTimeout:
    #    return get_session()
    return pr

def generate_random_ip():
    return f"{random.randint(1, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(1, 254)}"

if __name__ == '__main__':
    pr = get_session()
    print(pr)
    
    r=get('https://ip.oxylabs.io', proxies={'http':pr,'https':pr})
    print(r.text)
    
    
    