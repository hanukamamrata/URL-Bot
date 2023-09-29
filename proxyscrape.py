from requests import get
from random import choices, randint
from string import ascii_letters, digits

def get_session():
    st=''.join(choices(ascii_letters+digits, k=randint(8,20)))
    return f'http://73738zbpcibedc0-session-{st}-lifetime-10:okjz6fk9nkkx3rc@rp.proxyscrape.com:6060'

