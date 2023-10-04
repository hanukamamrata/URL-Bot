from seleniumwire import webdriver
from selenium.webdriver.common.by import By
from selenium_recaptcha.components import find_until_located, find_until_clicklable
from seleniumwire.utils import decode
from time import sleep
from urllib.parse import urlparse
from ad_blocker import is_ads

ua='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36'

# data:,

def run_bot(main_link, main_domain, main_referer, final_domain, bypass_referer, proxy=None, headless=True):
    def request_interceptor(request):
        url = request.url
        del request.headers['User-Agent']
        request.headers['User-Agent'] = ua
        
        if is_ads(url):
            request.create_response(
                status_code=403,
                body=''
            )
        elif '.css' in url:
            request.create_response(
                status_code=200,
                body=''
            )
        if urlparse(main_referer).netloc in url:
            request.create_response(
                status_code=200,
                body=f'<a href="{main_link}">Continue</a>'
            )
        '''if final_domain in url:
            request.headers['Referer'] = bypass_referer'''

    def response_interceptor(request, response):
        if '/links/go' in request.url:
            body=decode(response.body, response.headers.get('Content-Encoding', 'identity')).decode()
            print(main_domain+':', body)
    
    
    options = webdriver.ChromeOptions()
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    options.add_argument('--blink-settings=imagesEnabled=false')
    options.add_argument("--remote-debugging-port=9222")
    if headless:
        options.add_argument('--headless=new')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
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
    driver.response_interceptor=response_interceptor
        
    driver.maximize_window()
    print("Opening Mocked URL...")
    driver.get(main_referer)
    find_until_clicklable(driver, By.CSS_SELECTOR, 'a').click()
    print("Redirecting with Main Referer Header...")
    sleep(5)
    dps = driver.page_source
    if '502 Bad Gateway' in dps or '403 Forbidden' in dps or 'Check your proxy settings' in dps:
        raise Exception(str(driver.page_source))
    print('Completing 1st Page...')
    try:
        # sleep(int(find_until_located(driver, By.CSS_SELECTOR, '#yuidea-time').text))
        # find_until_clicklable(driver, By.CSS_SELECTOR, "#yuidea").click()
        driver.execute_script("document.cookie='cap_y2=10';document.cookie='cap_y=;expires=Thu, 01 Jan 1970 00:00:01 GMT';window.location.reload()")
    except:
        import traceback
        raise Exception(traceback.format_exc() + '\n\n' + driver.page_source)
    print('Completing 2nd Page...')
    sleep(3)
    driver.execute_script("window.open = (url) => {window.location.href = url}")
    find_until_clicklable(driver, By.CSS_SELECTOR, "#yuidea-snp button").click()
    print('Completing 3rd Page...')
    sleep(3)
    sleep(int(find_until_located(driver, By.CSS_SELECTOR, "#wpsafe-time").text))
    find_until_clicklable(driver, By.CSS_SELECTOR, "#btn6").click()
    print("Opening Final Page...")
    print('Finding button...')
    try:
        get_link_button=find_until_located(driver, By.CSS_SELECTOR, ".get-link")
    except:
        raise Exception(driver.page_source + '\n' + driver.current_url)
    print('Waiting for timer...')
    sleep(int(find_until_located(driver, By.CSS_SELECTOR, '#timer').text))
    #driver.execute_script("window.dispatchEvent(new Event('focus'))")
    found=False
    attempt=0
    while not found:
        if "Get Link".lower() in get_link_button.text.lower():
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
    from proxyscrape import get_session
    main_link = 'https://linkpays.in/DwbVBo2'
    main_domain = 'linkpays.in'
    main_referer = 'https://www.techlandbd.com/'
    final_domain = 'tech.smallinfo.in/Gadget'
    bypass_referer = 'https://loan.insuranceinfos.in'
    proxy=get_session()
    run_bot(main_link, main_domain, main_referer, final_domain, bypass_referer, proxy=proxy, headless=True)

