import kobo_crawler
import gcal
from datetime import date

if __name__ == '__main__':
    articles = kobo_crawler.get99Articles();
    if (not len(articles)):
        print('no artcles')
        exit(0)

    link = articles[0]['link']
    books = kobo_crawler.getArticleBooks(link)
    print(books)
    if (not len(books)):
        print('no books')
        exit(0)

    # dates = sorted([book['saleDate'] for book in books])
    # events = gcal.list_events(dates[0], dates[-1])

    # for book in books:
    #     if gcal.eventByBookId(events, book['id']): continue;
    #     gcal.create_event(book)
