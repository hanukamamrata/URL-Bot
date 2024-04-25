from time import sleep
from DrissionPage import ChromiumPage, ChromiumOptions
from DrissionPage.errors import ElementNotFoundError


def run_udlinks_bot(link, proxy=None, headless=None):
    options = ChromiumOptions()
    options.auto_port()
    options.set_argument('--start-maximized', True)

    page = ChromiumPage(options)
    page.set.cookies({'FCCDCF': '%5Bnull%2Cnull%2Cnull%2C%5B%22CP9oCIAP9oCIAEsACBENAxEoAP_gAEPgABBoINJB7D7FbSFCwH5zaLsAMAhHRsCAQoQAAASBAmABQAKQIAQCgkAQFASgBAACAAAAICZBIQIECAAACUAAQAAAAAAEAAAAAAAIIAAAgAEAAAAIAAACAAAAEAAIAAAAEAAAmAgAAIIACAAAhAAAAAAAAAAAAAAAAgAAAAAAAAAAAAAAAAAAAQOhQD2F2K2kKFkPCmQWYAQBCijYEAhQAAAAkCBIAAgAUgQAgFIIAgAIFAAAAAAAAAQEgCQAAQABAAAIACgAAAAAAIAAAAAAAQQAAAAAIAAAAAAAAEAAAAAAAQAAAAIAABEhCAAQQAEAAAAAAAQAAAAAAAAAAABAAA%22%2C%222~2072.70.89.93.108.122.149.196.2253.2299.259.2357.311.313.323.2373.358.2415.415.449.2506.2526.486.494.495.2568.2571.2575.540.574.2624.609.2677.827.864.981.1029.1048.1051.1095.1097.1126.1205.1211.1276.1301.1365.1415.1423.1449.1570.1577.1598.1651.1716.1735.1753.1765.1870.1878.1889.1958~dv.%22%2C%227B3D73E2-90F8-46B7-8CCE-E33E712FF338%22%5D%5D',
                      'FCNEC': '%5B%5B%22AKsRol8WO6rPyKTA90he16xJ31nwhP3SGaK9Bdrr0PUHdxCJy3qcCcGt0TXz2YeHqRlYFAwyrqH-XxOQev196qBDntDcRpPq2x1cU-Q2ukq_Zwcg1jh4qSjzNZ6KQN3mzyGfPjNCnNMCQb6Zg-ourqo9tKJFxbXwaw%3D%3D%22%5D%5D',
                      'domain': '.urbanpincode.com'})
    page.get('https://freegamer.blogspot.com/robots.txt')
    page.run_js(f'window.location.href = "{link}"')
    sleep(2)
    page.wait.doc_loaded()
    if '403 Forbidden' in page.title:
        page.quit()
        raise Exception('UDLinks: IP not allowed. 403 Forbidden Error!')
    while 1:
        if 'Redirecting pls wait' in page.html: sleep(1)
        else: break
    sleep(2)
    page.wait.doc_loaded()
    page.run_js('document.querySelector("#tp98").click()')
    sleep(2)
    page.wait.doc_loaded()
    btn6 = page.ele('#btn6')
    if not btn6:
        page.quit()
        raise Exception('UDLinks: `Continue` button is not found.')
    while btn6:
        page.run_js('''[...document.querySelectorAll('[style*="none"]')].forEach(function(e){e.removeAttribute('style')})''')
        try:
            btn6 = page.ele('#btn6')
            if btn6: btn6.click()
        except ElementNotFoundError:
            pass
        sleep(5)
    
    getLink = page.ele('css:.get-link')
    if not getLink:
        page.quit()
        raise Exception('UDLinks: Get Link button not found!')
    page.run_js(bypassFocusTimerJS)
    disabled = True
    while disabled: disabled = page.run_js("document.querySelector('.get-link').classList.contains('disabled')", as_expr=True)
    getLink.click()
    sleep(3)
    page.quit()
    print('UDLinks:', 'All Done')
    
        

bypassFocusTimerJS = '''for (event_name of ["visibilitychange", "webkitvisibilitychange", "blur"]) {window.addEventListener(event_name, function(event) {event.stopImmediatePropagation()}, true)} Object.defineProperty(document, 'visibilityState', {value: 'visible', writable: true});Object.defineProperty(document, 'hidden', {value: false, writable: true});document.dispatchEvent(new Event("visibilitychange"));'''


if __name__=='__main__':
    #from proxyscrape import get_session
    from all_links import random_udlinks
    print(random_udlinks)
    run_udlinks_bot(random_udlinks)


