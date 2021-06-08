import requests
from hashlib import md5
from datetime import date
from pathlib import Path
from bs4 import BeautifulSoup

def get99Articles():
    host = 'https://tw.news.kobo.com'
    # html_doc = requests.get(host + '/%E5%B0%88%E9%A1%8C%E4%BC%81%E5%8A%83/%E5%A5%BD%E8%AE%80%E6%9B%B8%E5%96%AE').text
    filename = Path("./kobo_list.htm").resolve()
    with open(filename) as f:
        html_doc = f.read()

    soup = BeautifulSoup(html_doc, 'html.parser')

    items = []
    for item in soup.select('.blog-item'):
        title = item.select_one('.blog-item-text-title:-soup-contains("一週99")');
        if title is None:
            continue

        items.append({
            "link": host + item.select_one("a.blog-item-container").get('href'),
            "title": title.string.strip(),
        })
    return items

def getArticleBooks(link):
    # html_doc = requests.get(link).text
    filename = Path("./kobo_article.htm").resolve()
    with open(filename) as f:
        html_doc = f.read()

    soup = BeautifulSoup(html_doc, 'html.parser')

    books = []
    for p in soup.select(".article-body p:has(> span + a[title])"):
        saleDate = parseSaleDate(p.select('span'))
        if (not isinstance(saleDate, date)): continue

        href = p.a.get('href')
        if (any(book['bookLink'] == href for book in books)): continue

        title = stripbrackets(p.a.get('title'))
        books.append({
            "id": md5(href.encode()).hexdigest(),
            "title": title,
            "saleDate": saleDate,
            "bookLink": href,
            "blogLink": link,
        })
    return books

def parseSaleDate(elements):
    try:
        dateString = "".join(list(map(lambda span: "" if span.string is None else span.string, elements))).split()
        if not len(dateString): return None

        (month, day) = dateString[0].split('/')
        return date.today().replace(month=int(month), day=int(day))
    except:
        return None

def stripbrackets(text, prefix="《", suffix="》"):
    if text.startswith(prefix):
        text = text[len(prefix):]
    if text.endswith(suffix):
        text = text[0: len(suffix) * -1]
    return text