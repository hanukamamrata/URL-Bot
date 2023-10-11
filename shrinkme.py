import seleniumwire.undetected_chromedriver as uc
from selenium_recaptcha.components import find_until_located, find_until_clicklable
from selenium.webdriver.common.by import By
from ad_blocker import is_ads
from seleniumwire.utils import decode
from time import sleep


def run_shrinkme_bot(link, proxy=None, headless=True):
    def request_interceptor(request):
        url = request.url
        if is_ads(url):
            request.create_response(status_code=403)
    
    def response_interceptor(request, response):
        if '/links/go' in request.url:
            body=decode(response.body, response.headers.get('Content-Encoding', 'identity')).decode()
            print('ShrinkMe:', body)


    options = uc.ChromeOptions()
    if headless:
        options.add_argument('--headless=new')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-notifications')
    options.add_argument("--remote-debugging-port=9222")
    options.add_argument('--ignore-ssl-errors=yes')
    options.add_argument('--ignore-certificate-errors')
    options.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2})
    
    seleniumwire_options = {
        'proxy': {
            'http': proxy,
            'https': proxy
        }
    }
    
    driver = uc.Chrome(options=options, seleniumwire_options=seleniumwire_options)
    
    driver.maximize_window()
    driver.get('https://thekisscartoon.com/post-sitemap.xml')
    driver.execute_script(f'window.location.href="{link}"')
    sleep(3)
    driver.execute_script(f'window.location.href="https://themezon.net/link.php?link={link.split("/")[-1]}"')
    sleep(3)
    driver.execute_script(f'window.location.href="https://en.shrinke.me/{link.split("/")[-1]}"')
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
    from all_links import random_shrinkme
    run_shrinkme_bot(random_shrinkme, headless=False)


