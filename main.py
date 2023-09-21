#from v2links import run_v2links_bot
from exurl import run_exurl_bot
from linkpays import run_linkpays_bot
from bindaslinks import run_bindaslinks_bot
#from shrinkearn import run_shrinkearn_bot
from all_links import random_v2links, random_exurl, random_shrinkearn, random_linkpays, random_bindaslinks
import urllib3, threading
Thread=threading.Thread

d={'e':''}

def excepthook(l):
    d['e']+=str(l.exc_value) + '\n\n'

threading.excepthook=excepthook

def main(proxy=None, **kw):
    t=[]
    for i in range(3):
        t.append(Thread(target=lambda: run_exurl_bot(random_exurl, proxy, **kw)))
    
    t.append(Thread(target=lambda: run_linkpays_bot(random_linkpays, proxy, **kw)))
    t.append(Thread(target=lambda: run_bindaslinks_bot(random_bindaslinks, proxy, **kw)))
    
    for v in t:
        v.start()
    for v in t:
        v.join()
        
    if d['e']!='':
        raise Exception(d['e'])



if __name__ == '__main__':
    main()
