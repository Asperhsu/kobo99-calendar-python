import kobo_crawler
import gcal

def lambda_handler(event, context):
    # get articles about 99 sale
    articles = kobo_crawler.fetch_articles();
    if (not len(articles)):
        print('no artcles')
        exit(0)

    # get first (latest) article to retrive books info
    link = articles[0]['link']
    books = kobo_crawler.fetch_books(link)
    if (not len(books)):
        print('no books')
        exit(0)

    # get exists event between dates for check if exists
    dates = sorted([book['date'] for book in books])
    events = gcal.list_events(dates[0], dates[-1])

    for book in books:
        if gcal.event_by_book_id(events, book['id']): continue;
        gcal.create_event(book)

    return "done"

if __name__ == "__main__":
    lambda_handler('', '')