from requests import get
from random import choices, randint, choice
from string import ascii_letters, digits
import requests, random

def get_session():
    countries = ['us', 'gb', 'au', 'ca', 'in', 'mx', 'nz']
    country = choice(countries) 
    st = ''.join(choices(digits, k=randint(8,20)))
    country=country.upper()
    pr = f'http://11031539-res-country-{country}-session-{st}:ps2ah00tr@190.2.143.237:14504'
    return pr

def generate_random_ip():
    return f"{random.randint(1, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(1, 254)}"

if __name__ == '__main__':
    pr = get_session()
    print(pr)
    
    r=get('https://ip.oxylabs.io', proxies={'http':pr,'https':pr})
    print(r.text)
    
    
    