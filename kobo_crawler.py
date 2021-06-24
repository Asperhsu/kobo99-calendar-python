import requests
from hashlib import md5
from datetime import date
from bs4 import BeautifulSoup

def fetch_articles():
    print('fetch articles list')
    host = 'https://tw.news.kobo.com'
    html = requests.get(host + '/%E5%B0%88%E9%A1%8C%E4%BC%81%E5%8A%83/%E5%A5%BD%E8%AE%80%E6%9B%B8%E5%96%AE').text

    soup = BeautifulSoup(html, 'html.parser')

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

def fetch_books(link):
    print('find books in: ' + link)
    html = requests.get(link).text
    soup = BeautifulSoup(html, 'html.parser')

    books = []
    for p in soup.select('.article-body p:-soup-contains("選書")'):
        sale_date = parse_sale_date(p.select('span'))
        if (not isinstance(sale_date, date)): continue

        # book link
        try: book_link = p.a.get('href')
        except: continue;

        id = md5(book_link.encode()).hexdigest()
        if (any(book['id'] == id for book in books)): continue

        title = strip_brackets(p.a.get('title'))
        description = format_description(soup, book_link, link)

        books.append({
            "id": id,
            "date": sale_date,
            "title": title,
            "description": description,
        })
    return books

def parse_sale_date(elements):
    try:
        date_str = "".join(list(map(lambda span: "" if span.string is None else span.string, elements))).split()
        if not len(date_str): return None

        (month, day) = date_str[0].split('/')
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

    # cover
    img = soup.select_one(f'a[href="{book_link}"] > img')
    if (not img is None):
        descs.append(img.prettify())

    # box description
    for p in soup.select(f'div.simplebox-content:has(a[href="{book_link}"]) > p'):
        descs.append('<div>' + p.encode_contents().decode('utf-8') + '</div>')

    descs.append(f'<div>來源：<a href="{blog_url}">{blog_url}</a></div>')

    return "".join(descs)
