import requests

from selenium.webdriver import Chrome
from urllib.parse import unquote

from selenium import webdriver

from samsung_dot_com_html_parser import SamsungDotComHTMLParser

op = webdriver.ChromeOptions()
op.add_argument("--headless")

driver = Chrome(executable_path="C://WebDriver//bin//chromedriver.exe", options=op)


def handle_current_page(page_url):
    print("this page: ", page_url)
    driver.get(page_url)
    net_data = driver.execute_script("var performance = window.performance "
                                     "|| window.mozPerformance "
                                     "|| window.msPerformance "
                                     "|| window.webkitPerformance "
                                     "|| {}; var network = performance.getEntries() "
                                     "|| {}; return network;")

    smetric = list(filter(lambda x: "smetric" in x['name'], net_data))
    page_attributes = dict()
    try:
        for s in smetric[-1]['name'].split('?')[1].split('&'):
            if "v40" in s or "c6" in s or "c39" in s:
                s = unquote(s)
                k, v = s.split("=")
                page_attributes[k] = v
    except IndexError:
        print("indexError", page_url, smetric)

    response = requests.get(page_url)
    html_parser = SamsungDotComHTMLParser()
    html_parser.feed(response.text)
    html_parser.close()

    return page_attributes, html_parser.next_page

queue = []
visited = set()
links = []

queue.append("http://www.samsung.com/uk/offer/samsung-s20-sero-lifestyle-tv-deal/")

while len(queue) != 0:
    current_page = queue.pop(0)
    page_attr, next_pages = handle_current_page(current_page)
    if not page_attr:
        print("page_Attr none")
        continue
    visited.add(page_attr['c39'])
    print(page_attr['c39'])

    for next_page in next_pages:
        url: str = next_page['href'].strip(" ")
        if url.startswith("//"):
            url = url[2:]
        elif url.startswith("/"):
            url = f'http://www.samsung.com{url}'
        elif url.startswith("www"):
            url = f'http://{url}'

        links.append((current_page, next_page, f'{next_page["class"]},{next_page["an_ac"]},{next_page["an_ca"]},{next_page["an_la"]},'))
        if url not in visited and url not in queue:
            queue.append(url)


print(links)