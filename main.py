from cloudscraper import CloudScraper as Session
from all_links import *
# from telegramlinks import run_telegram_bot
from teraboxlinks import run_terabox_bot
# from udlinks import run_udlinks_bot
from malink import run_malink_bot
# from zagl import run_zagl_bot
from random import randint
import urllib3, threading
Thread=threading.Thread

d={'e':''}

def excepthook(l):
    d['e']+=str(l.exc_value) + '\n\n'

def isDuplicate():
    ip = Session().get('https://ip.oxylabs.io').text
    return ip in Session().get('https://ip-limiter-server.onrender.com/used').text

def addToDB():
    ip = Session().get('https://ip.oxylabs.io').text.replace('\n', '')
    return 'true' in Session().get('https://ip-limiter-server.onrender.com/add?ip=' + ip).text

threading.excepthook=excepthook

def main(proxy=None, **kw):
    t=[]
    # t.append(Thread(target=lambda: run_adrino_bot(random_adrino, proxy, **kw)))
    # t.append(Thread(target=lambda: run_nano_bot(random_nanolinks, proxy, **kw)))
    t.append(Thread(target=lambda: run_terabox_bot(random_teraboxlinks, proxy, **kw)))
    # t.append(Thread(target=lambda: run_zagl_bot(random_zagl, proxy, **kw)))
    if not isDuplicate():
        # t.append(Thread(target=lambda: run_telegram_bot(random_telegramlinks, None, **kw)))
        # t.append(Thread(target=lambda: run_udlinks_bot(random_udlinks, None, **kw)))
        t.append(Thread(target=lambda: run_malink_bot(random_malink, None, **kw)))
        addToDB()
    else: print('Skipping some thread for duplicate view.')

    for v in t: v.start()
    for v in t: v.join()
        
    if d['e']!='': raise Exception(d['e'])
    # Slow earning speed
    from time import sleep
    sleep(40)



if __name__ == '__main__':
    main()
