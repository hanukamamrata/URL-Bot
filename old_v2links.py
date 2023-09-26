from seleniumwire import webdriver
from selenium.webdriver.common.by import By
from selenium_recaptcha.components import find_until_located
from time import sleep
from ad_blocker import is_ads

def run_v2links_bot(link:str, proxy=None, headless=True):
    def request_interceptor(request):
        url = request.url
        if is_ads(url):
            request.create_response(
                status_code=403,
                body=''
            )
        if 'vzu.us' in url:
            request.headers['Referer'] = 'https://gadgetsreview27.com'
        # if url.startswith('https://'):
            # request.url = request.url.replace('https://', 'http://')
    
    options = webdriver.ChromeOptions()
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    options.add_argument("--remote-debugging-port=9222")
    if headless:
        options.add_argument('--headless=new')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-gpu')
    options.add_argument('--ignore-ssl-errors')
    options.add_argument('--disable-notifications')

    seleniumwire_options = {
        'proxy': {
            'http': proxy,
            'https': proxy,
        }
    }
    
    print('Opening Browser...')
    if proxy:
        driver = webdriver.Chrome(options=options, seleniumwire_options=seleniumwire_options)
    else:
        driver = webdriver.Chrome(options=options)
    driver.request_interceptor = request_interceptor
        
    driver.maximize_window()
    print("Opening URL...")
    driver.get(link.replace('v2links.com', 'vzu.us'))
    dps = driver.page_source
    if '502 Bad Gateway' in dps or '403 Forbidden' in dps or 'Check your proxy settings' in dps:
        raise Exception(str(driver.page_source))
    print('Finding button...')
    try:
        get_link_button=find_until_located(driver, By.CSS_SELECTOR, ".get-link")
    except:
        raise Exception(driver.page_source + '\n' + driver.current_url)
    print('Waiting for timer...')
    sleep(5)
    #driver.execute_script("window.dispatchEvent(new Event('focus'))")
    found=False
    attempt=0
    while not found:
        if "Get Link" in get_link_button.text:
            found=True
            try:
                driver.execute_script("document.querySelector('.get-link').click()")
            except:
                pass
            break
        sleep(2)
        attempt+=1
        if attempt >= 20:
            raise Exception(f"40 sec waited but link doesn't appear. Button text is '{get_link_button.text}'")
    print("Step Completed!")

    sleep(5)
    driver.quit()

if __name__ == "__main__":
    from all_links import random_v2links
    run_v2links_bot(random_v2links, headless=False)

