import time, requests, whisper, warnings, os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
warnings.filterwarnings("ignore")

model = whisper.load_model("base.en")

def find_until_located(driver,find_by,name,timeout=10):
	return WebDriverWait(driver, timeout).until(EC.presence_of_element_located((find_by, name)))

def find_until_clicklable(driver,find_by,name,timeout=10):
	return WebDriverWait(driver, timeout).until(EC.element_to_be_clickable((find_by, name)))

def scroll_to_element(driver,element):
	driver.execute_script("arguments[0].scrollIntoView();", element)

# rc-audiochallenge-error-message

class Solve_Recaptcha():
    def __init__(self, driver, output=False) -> None:
        self.driver = driver
        self.output=output
        self.run_solver()
        
    def o(self, *a, **kw):
        kw['end']=''
        if self.output: print(*a, **kw)
        
    def transcribe(self, url):
        with open('.temp', 'wb') as f:
            self.o('\rDownloading Audio...')
            f.write(requests.get(url).content)
        self.o('\rTranscribing Audio...')
        result = model.transcribe('.temp')
        os.remove('.temp')
        return result["text"].strip()

    def click_checkbox(self):
        driver=self.driver
        driver.switch_to.default_content()
        self.o('\rClicking Checkbox...')
        driver.switch_to.frame(find_until_located(driver, By.XPATH, ".//iframe[@title='reCAPTCHA']"))
        find_until_clicklable(driver, By.ID, "recaptcha-anchor-label").click()

    def request_audio_version(self):
        driver=self.driver
        driver.switch_to.default_content()
        self.o('\rSwitching to Audio...')
        driver.switch_to.frame(find_until_located(driver, By.XPATH, ".//iframe[@title='recaptcha challenge expires in two minutes']"))
        find_until_clicklable(driver, By.ID, "recaptcha-audio-button").click()

    def solve_audio_captcha(self):
        driver=self.driver
        text = self.transcribe(find_until_located(driver, By.ID, "audio-source").get_attribute('src'))
        self.o('\rSending transcribe...')
        find_until_located(driver, By.ID, "audio-response").send_keys(text)
        find_until_clicklable(driver, By.ID, "recaptcha-verify-button").click()

    def check_blocking(self):
        driver=self.driver
        try:
            find_until_located(driver, By.CLASS_NAME, 'rc-doscaptcha-header-text')
        except KeyboardInterrupt: raise KeyboardInterrupt
        except:
            driver.switch_to.default_content()
            raise Exception('Unknown Error.')
        driver.switch_to.default_content()
        raise Exception('Request blocked by google.')

    def run_solver(self):
        scroll_to_element(self.driver, find_until_located(self.driver, By.XPATH, ".//iframe[@title='reCAPTCHA']"))
        self.click_checkbox()
        try:
            self.request_audio_version()
            self.solve_audio_captcha()
        except KeyboardInterrupt: raise KeyboardInterrupt
        except: self.check_blocking()

        self.o('\rRecaptcha Solved\n')
        driver.switch_to.default_content()

if __name__ == "__main__":
    from selenium import webdriver
    driver = webdriver.Chrome()
    driver.get("https://www.google.com/recaptcha/api2/demo")
    Solve_Recaptcha(driver, True)
    time.sleep(10)
    
    