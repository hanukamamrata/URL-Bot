from v2links import run_v2links_bot
from all_links import random_v2links
import urllib3, threading
Thread=threading.Thread

d={'e':''}

def excepthook(l):
    d['e']+=str(l.exc_value) + '\n\n'

threading.excepthook=excepthook

def main(proxy=None, **kw):
    t=[]
    #t.append(Thread(target=lambda: run_v2links_bot(random_v2links, proxy, **kw)))
    
    for v in t:
        v.start()
    for v in t:
        v.join()
        
    if d['e']!='':
        raise Exception(d['e'])



if __name__ == '__main__':
    main()
