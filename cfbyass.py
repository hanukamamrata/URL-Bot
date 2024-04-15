from DrissionPage import ChromiumPage, ChromiumOptions
from requests.cookies import RequestsCookieJar
import os, time, zipfile, shutil

def cfbypass(url:str, timeout:int=20, retry:int=3, proxy:str=None):
    nc = os.path.join(os.path.dirname(__file__), 'NopeCha')
    with zipfile.ZipFile(nc+'.zip', 'r') as f: f.extractall(nc)
    options = ChromiumOptions()
    options.auto_port()
    if proxy: options.set_proxy(proxy)
    options.set_argument('--start-maximized', True)
    options.add_extension(nc)
    # options.add_extension(os.path.join(os.path.dirname(__file__), 'header_modifier'))
    page = ChromiumPage(options)
    for i in range(retry):
        page.get(url)
        attempt = 0
        sleepTime = 3
        toBreakFor = False
        while 1:
            time.sleep(sleepTime)
            if not 'Ray ID' in page.html:
                toBreakFor = True
                break
            attempt += 1
            if attempt >= timeout / sleepTime:
                if i == retry - 1:
                    page.quit()
                    try:
                        shutil.rmtree(nc)
                    except FileNotFoundError:
                        pass
                    raise Exception(f'{timeout * retry} sec passed but cloudflare is still here.')
                break
        if toBreakFor: break

    cookies = page.cookies(0, 1, 0)
    ua = page.user_agent
    page.quit()
    try:
        shutil.rmtree(nc)
    except FileNotFoundError:
        pass
    jar = RequestsCookieJar()
    for i in cookies: jar.set(**i)
    return (ua, jar)


if __name__ == '__main__':
    user_agent, cookies = cfbypass('https://v2links.me/')
    print(user_agent)
    print(cookies)
