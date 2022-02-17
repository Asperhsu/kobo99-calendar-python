import requests
import re
from hashlib import md5
from datetime import date
from bs4 import BeautifulSoup

headers = {
    'Accept': 'text/html',
    'Host': 'www.kobo.com',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36 Edg/98.0.1108.55',
}

def fetch_articles():
    print('fetch articles list')
    html = requests.get('https://www.kobo.com/zh/blog', verify=False, timeout=10, headers=headers).text
    soup = BeautifulSoup(html, 'html.parser')

    items = []
    for item in soup.select('.card'):
        title = item.select_one('.card__title:-soup-contains("一週99")');
        if title is None:
            continue

        items.append({
            "link": item.select_one("a.card__link").get('href'),
            "title": title.string.strip(),
        })
    return items

def fetch_books(link):
    print('find books in: ' + link)
    html = requests.get(link, verify=False, timeout=10, headers=headers).text
    soup = BeautifulSoup(html, 'html.parser')

    books = []
    for p in soup.select('.content-block p:-soup-contains("選書")'):
        sale_date = parse_sale_date(p)
        if (not isinstance(sale_date, date)): continue

        # book link
        try: book_link = p.a.get('href')
        except: continue

        id = md5(book_link.encode()).hexdigest()
        if (any(book['id'] == id for book in books)): continue

        title = strip_brackets(p.a.string.strip())
        description = format_description(soup, book_link, link)

        books.append({
            "id": id,
            "date": sale_date,
            "title": title,
            "description": description,
        })
    return books

def parse_sale_date(p):
    try:
        match = re.findall(r'^([0-9]{1,2}\/[0-9]{1,2}).+選書', p.get_text(), re.MULTILINE)
        if match is None: return None
        if len(match) == 0: return None

        (month, day) = match[0].split('/')
        return date.today().replace(month=int(month), day=int(day))
    except:
        return None

def strip_brackets(text, prefix="《", suffix="》"):
    if text.startswith(prefix):
        text = text[len(prefix):]
    if text.endswith(suffix):
        text = text[0: len(suffix) * -1]
    return text

def format_description(soup, book_link, blog_url):
    descs = []

    # find book-block
    anchor = soup.select_one(f'article .book-block a[href="{book_link}"]')
    if (anchor is None): return ""

    block = anchor.find_parent('div', class_='book-block')
    if (block is None): return ""

    # get img html
    img = block.select_one('img')
    if (not img is None):
        src = img.get('src')
        descs.append(f'<img src="{src}" width="100%" height="auto">')

    # get title
    title = block.select_one('span.title')
    if (not title is None):
        descs.append(f'<div><a href="{book_link}">{title.string.strip()}</a></div>')

    # get authot
    author = block.select_one('span.author')
    if (not author is None):
        descs.append('<div>' + author.encode_contents().decode('utf-8') + '</div>')

    # other infomation (publisher, coupon...)
    for p in block.select('p'):
        descs.append('<div>' + p.encode_contents().decode('utf-8') + '</div>')

    descs.append(f'<div><a href="{blog_url}">Kobo Blog</a></div>')
    return "".join(descs)
