
from cloudscraper import CloudScraper as Session
from DrissionPage import ChromiumPage, ChromiumOptions

def isDuplicate():
    ip = Session().get('https://ip.oxylabs.io').text
    return ip in Session().get('https://ip-limiter-server.onrender.com/used').text

def addToDB():
    ip = Session().get('https://ip.oxylabs.io').text.replace('\n', '')
    return 'true' in Session().get('https://ip-limiter-server.onrender.com/add?ip=' + ip).text

def run_telegram_bot(link, proxy=None, headless=None):
    d = isDuplicate()
    if d: print('Error in TelegramLinks: Duplicate View')
    options = ChromiumOptions()
    options.auto_port()
    options.set_argument('--start-maximized', True)

    page = ChromiumPage(options)
    page.get(link)
    if not d: addToDB()
    print('Telegram Links:', 'All Done')
    


if __name__=='__main__':
    #from proxyscrape import get_session
    from all_links import random_telegramlinks
    print(random_telegramlinks)
    run_telegram_bot(random_telegramlinks)


