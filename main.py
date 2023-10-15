from all_links import *
from directlink import run_directlink_bot
import urllib3, threading
Thread=threading.Thread

d={'e':''}

def excepthook(l):
    d['e']+=str(l.exc_value) + '\n\n'

threading.excepthook=excepthook

def main(proxy=None, **kw):
    t=[]
    #t.append(Thread(target=lambda: run_directlink_bot(random_directlink, proxy, **kw)))
    
    for v in t:
        v.start()
    for v in t:
        v.join()
        
    if d['e']!='':
        raise Exception(d['e'])



if __name__ == '__main__':
    main()
