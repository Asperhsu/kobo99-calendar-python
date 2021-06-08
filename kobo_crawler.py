import requests
from hashlib import md5
from datetime import date
from bs4 import BeautifulSoup

def get99Articles():
    print('fetch articles')
    host = 'https://tw.news.kobo.com'
    html_doc = requests.get(host + '/%E5%B0%88%E9%A1%8C%E4%BC%81%E5%8A%83/%E5%A5%BD%E8%AE%80%E6%9B%B8%E5%96%AE').text

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
    print('fetch article: ' + link)
    html_doc = requests.get(link).text
    soup = BeautifulSoup(html_doc, 'html.parser')

    books = []
    for p in soup.select('.article-body p:-soup-contains("選書")'):
        saleDate = parseSaleDate(p.select('span'))
        if (not isinstance(saleDate, date)): continue

        # book link
        try: bookLink = p.a.get('href')
        except: continue;
        if (any(book['bookLink'] == bookLink for book in books)): continue

        title = stripbrackets(p.a.get('title'))
        description = formatDescription(soup, bookLink)

        books.append({
            "id": md5(bookLink.encode()).hexdigest(),
            "date": saleDate,
            "title": title,
            "description": description,
            "bookLink": bookLink,
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

def formatDescription(soup, bookLink):
    descs = []

    # cover
    img = soup.select_one(f'a[href="{bookLink}"] > img')
    if (not img is None):
        descs.append(img.prettify())

    # box description
    box = soup.select_one(f'div.simplebox-content:has(a[href="{bookLink}"])');
    for p in box.find_all('p', recursive=False):
        desc = ""
        for content in p.contents:
            if content.name is None:
                desc += content
            elif content.name == 'a':
                desc += f'<a href="{content.get("href")}">{content.string}</a>'
            elif content.name == 'span':
                desc += content.string
        descs.append('<div>' + desc + '</div>')

    return "".join(descs)
