import requests

from selenium.webdriver import Chrome
from urllib.parse import unquote

from samsung_dot_com_html_parser import SamsungDotComHTMLParser

driver = Chrome(executable_path="C://WebDriver//bin//chromedriver.exe")


def handle_current_page(page_url):
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
        print("indexError", smetric)

    response = requests.get(page_url)
    html_parser = SamsungDotComHTMLParser()
    html_parser.feed(response.text)
    html_parser.close()

    return page_attributes, html_parser.next_page

queue = []
visited = set()

queue.append("http://www.samsung.com/uk")

while len(queue) != 0:
    current_page = queue.pop(0)
    page_attr, next_pages = handle_current_page(current_page)
    if not page_attr:
        print("page_Attr none", next_pages)
        continue
    visited.add(page_attr['c39'])
    print(page_attr['c39'])

    for next_page in next_pages:
        url: str = next_page['href']
        if not url.startswith(('www', 'http://')):
            url = f'http://www.samsung.com{url}'
        if url not in visited:
            queue.append(url)
