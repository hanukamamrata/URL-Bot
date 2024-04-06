from requests import get
from random import choices, randint, choice
from string import ascii_letters, digits
import requests, random

def get_session():
    countries = ['us', 'gb', 'au', 'ca', 'in', 'mx', 'nz']
    country = choice(countries) 
    st = ''.join(choices(digits, k=randint(8,20)))
    # country=country.upper()
    pr = f'http://0d2zysdt2i8716o-country-{country}-session-{st}-lifetime-10:p42bzwxrl6jqcwz@rp.proxyscrape.com:6060'
    return pr

def generate_random_ip():
    return f"{random.randint(1, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(1, 254)}"

if __name__ == '__main__':
    pr = get_session()
    print(pr)
    
    r=get('https://ip.oxylabs.io', proxies={'http':pr,'https':pr})
    print(r.text)
    
    
    