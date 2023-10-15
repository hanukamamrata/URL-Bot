import undetected_chromedriver as uc
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from os import path
import os
from time import sleep

def run_directlink_bot(link, proxy=None, headless=True):
    try: __file__
    except: __file__ = os.getcwd()
    
    base_dir=path.dirname(path.abspath(__file__))
    prext_dir=path.join(base_dir, 'pr_ext')
    
    if proxy:
        up, hp = proxy.replace('http://','').replace('https://','').split('@')
        username, password = up.split(':')
        host, port = hp.split(':')
        
        try:
            os.mkdir(prext_dir)
        except FileExistsError:
            pass
        
        manifest_json = """
            {
                "version": "1.0.0",
                "manifest_version": 2,
                "name": "Proxies",
                "permissions": [
                    "proxy",
                    "tabs",
                    "unlimitedStorage",
                    "storage",
                    "<all_urls>",
                    "webRequest",
                    "webRequestBlocking"
                ],
                "background": {
                    "scripts": ["background.js"]
                },
                "minimum_chrome_version":"22.0.0"
            }
        """
        
        background_js = """
            var config = {
                    mode: "fixed_servers",
                    rules: {
                    singleProxy: {
                        scheme: "http",
                        host: "%s",
                        port: parseInt(%s)
                    },
                    bypassList: ["localhost"]
                    }
                };
        
            chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});
        
            function callbackFn(details) {
                return {
                    authCredentials: {
                        username: "%s",
                        password: "%s"
                    }
                };
            }
        
            chrome.webRequest.onAuthRequired.addListener(
                        callbackFn,
                        {urls: ["<all_urls>"]},
                        ['blocking']
            );
        """ % (host, port, username, password)
        
        with open(path.join(prext_dir, "manifest.json"), 'w') as m_file:
            m_file.write(manifest_json)
        with open(path.join(prext_dir, "background.js"), 'w') as b_file:
            b_file.write(background_js)
    
    options = uc.ChromeOptions()
    if headless:
        options.add_argument('--headless=new')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-notifications')
    options.add_argument("--remote-debugging-port=9222")
    options.add_argument('--ignore-ssl-errors=yes')
    options.add_argument('--ignore-certificate-errors')
    options.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2}) # Block all images
    if proxy:
        options.add_argument(f'--load-extension={prext_dir}')
    
    driver = uc.Chrome(version_main=117, options=options)
    driver.maximize_window()
    driver.get(link)
    if 'Anonymous Proxy detected' in driver.page_source:
        raise Exception('Anonymous Proxy detected, So request blocked.')
    old_url = driver.current_url
    WebDriverWait(driver, 30).until(EC.url_changes(old_url))
    sleep(3)
    driver.quit()


if __name__=='__main__':
    from all_links import random_directlink
    run_directlink_bot(random_directlink, headless=False)


