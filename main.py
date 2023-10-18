from all_links import *
from directlink import run_directlink_bot
from shrinkforearn import run_shrinkforearn_bot
from v2links import run_v2links_bot
from random import randint
import urllib3, threading
Thread=threading.Thread

d={'e':''}

def excepthook(l):
    d['e']+=str(l.exc_value) + '\n\n'

threading.excepthook=excepthook

def main(proxy=None, **kw):
    t=[]
    t.append(Thread(target=lambda: run_v2links_bot(random_v2links, proxy=None, **kw)))
    #for i in range(randint(1,3)):
        #t.append(Thread(target=lambda: run_directlink_bot(random_directlink, proxy, **kw)))
    for i in range(randint(1,2)):
        t.append(Thread(target=lambda: run_shrinkforearn_bot(random_shrinkforearn, proxy, **kw)))
    
    for v in t:
        v.start()
    for v in t:
        v.join()
        
    if d['e']!='':
        raise Exception(d['e'])



if __name__ == '__main__':
    main()
