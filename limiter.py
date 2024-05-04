from requests import get 
import inspect


def get_date():
    r = get('https://worldtimeapi.org/api/timezone/Asia/Dhaka')
    dt = r.json().get('datetime', 'idk9910').split('T')[0]
    return dt

cur_date = get_date()

def isCompleted(t:int, idn:str):
    r = get(f'https://api.counterapi.dev/v1/{idn}/' + cur_date)
    c = int(r.json().get('count', 0))
    return True if c >= t else False

def submitOne(idn:str):
    r = get(f'https://api.counterapi.dev/v1/{idn}/{cur_date}/up')
    c = int(r.json().get('count', 0))
    return c

def getRecord(idn:str):
    r = get(f'https://api.counterapi.dev/v1/{idn}/' + cur_date)
    c = int(r.json().get('count', 0))
    return c

