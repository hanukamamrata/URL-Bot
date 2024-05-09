from mechanize import Browser
from urllib.parse import urlparse


def addTraffic(url1: str, url2: str, url3: str, gaID: str):
    br = Browser()
    br.set_handle_robots(False)
    br.set_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:125.0) Gecko/20100101 Firefox/125.0')
    br.open('https://traffic-creator.com/login')
    br.select_form(nr=0)
    br.form['username'] = 'flixwondersofficial@gmail.com'
    br.form['password'] = 'oeqSXFPgsXsQ'
    br.submit()
    br.open('https://traffic-creator.com/dashboard/buy.html?plan=nano&getfreenanocredit=')
    br.select_form(nr=0)
    br.form['title'] = urlparse(url1).netloc
    br.form['url'] = 'https://www.flixwonders.com/'
    br.submit()
    br.select_form(nr=0)
    br.form['ga_id'] = gaID
    br.form['traffic_type'] = ['organic']
    br.form['keywords'] = urlparse(url1).netloc
    br.form['url1'] = url1
    br.form['url2'] = url2
    br.form['url3'] = url3
    br.submit()

    open('test.html', 'wb').write(br.response().read())


addTraffic('https://file.urbanpincode.com/',
           'https://file.urbanpincode.com/exploring-the-university-of-massachusetts/',
           'https://file.urbanpincode.com/chamberlain-university-troy-shaping-the-future-of-healthcare-leadership/',
           'G-ZR64NJY7DW')


