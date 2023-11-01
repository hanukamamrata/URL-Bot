from all_links import *
from directlink import run_directlink_bot
from adrinolinks import run_adrino_bot
from random import randint
import urllib3, threading
Thread=threading.Thread

d={'e':''}

def excepthook(l):
    d['e']+=str(l.exc_value) + '\n\n'

threading.excepthook=excepthook

def main(proxy=None, **kw):
    t=[]
    #for i in range(randint(1,3)):
        #t.append(Thread(target=lambda: run_directlink_bot(random_directlink, proxy, **kw)))
    t.append(Thread(target=lambda: run_adrino_bot(random_adrino, proxy, **kw)))
    
    for v in t:
        v.start()
    for v in t:
        v.join()
        
    if d['e']!='':
        raise Exception(d['e'])
    
    # Slow earning speed
    from time import sleep
    sleep(120)



if __name__ == '__main__':
    main()
