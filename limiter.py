from requests import get 
import inspect

if __name__ == "__main__":
    fn == __file__
else:
    for frame in inspect.stack()[1:]:
        if frame.filename[0] != '<':
            fn = frame.filename
            break

idn = 'urlbot-' + fn.split('/')[-1].split('\\')[-1]

def get_date():
    r = get('https://worldtimeapi.org/api/timezone/Asia/Dhaka')
    dt = r.json().get('datetime', 'idk9910').split('T')[0]
    return dt

def isCompleted(t:int):
    r = get(f'https://api.counterapi.dev/v1/{idn}/' + get_date())
    c = int(r.json().get('count', 0))
    return True if c >= t else False

def submitOne():
    r = get(f'https://api.counterapi.dev/v1/{idn}/{get_date()}/up')
    c = int(r.json().get('count', 0))
    return c


