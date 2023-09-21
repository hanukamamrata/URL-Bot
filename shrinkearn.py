from seleniumwire import webdriver
from selenium.webdriver.common.by import By
from selenium_recaptcha.components import find_until_located
from time import sleep
from bs4 import BeautifulSoup
from ad_blocker import is_ads
import requests

def get_form_data(link:str):
    data = {i : None for i in ['token', 'c_d', 'c_t', 'alias']}
    resp = requests.get(link)
    soap = BeautifulSoup(resp.text, 'html.parser')
    for name in list(data):
        data[name] = soap.select_one(f'input[name="{name}"]').get('value')
    return data

def run_shrinkearn_bot(link:str, proxy=None, headless=True):
    def request_interceptor(request):
        url = request.url
        if is_ads(url):
            request.create_response(
                status_code=403,
                body=''
            )
        if 'tii.la' in url:
            if request.headers.get('Referer'): del request.headers['Referer']
            request.headers['Referer'] = 'https://blogtechh.com/'
        # if url.startswith('https://'):
            # request.url = request.url.replace('https://', 'http://')
    
    form_data = get_form_data(link)
    form_html = f'<form action="{link}" method="POST">'
    for name, value in form_data.items():
        form_html += f'<input type="hidden" name="{name}" value="{value}">'
    form_html += '<input type="submit" value="Goo" id="submit">'
    form_html += '</form>'
    
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
    driver.get("data:text/html;charset=utf-8," + form_html)
    find_until_located(driver, By.ID, 'submit').click()
    dps = driver.page_source
    if '502 Bad Gateway' in dps or '403 Forbidden' in dps or 'Check your proxy settings' in dps:
        raise Exception(str(driver.page_source))
    print('Finding button...')
    try:
        get_link_button=find_until_located(driver, By.CSS_SELECTOR, ".get-link")
    except:
        raise Exception(driver.page_source + '\n' + driver.current_url)
    
    driver.execute_script("try{document.querySelector('.get-link').removeAttribute('onclick')}catch{void(0)}")
    print('Waiting for timer...')
    sleep(10)
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
    from all_links import random_shrinkearn
    run_shrinkearn_bot(random_shrinkearn, headless=False)

