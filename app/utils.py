import requests

def fetch_book_metadata(title):
    """
    Fetch book metadata from OpenLibrary API
    """
    url = f"https://openlibrary.org/search.json?title={title}"
    response = requests.get(url)
    if response.status_code != 200:
        return None
    data = response.json()
    if data['docs']:
        book = data['docs'][0]
        return {
            "title": book.get('title', ''),
            "author": book.get('author_name', [''])[0] if book.get('author_name') else '',
            "total_pages": book.get('number_of_pages_median', 0),
            "genre": book.get('subject', [''])[0] if book.get('subject') else ''
        }
    return None
def calculate_metrics(pages_read, reading_time_minutes, total_pages=0):
    """
    Calculates reading speed and progress
    """
    if reading_time_minutes > 0:
        speed = pages_read / (reading_time_minutes / 60)  # pages per hour
    else:
        speed = 0

    if total_pages > 0:
        progress = (pages_read / total_pages) * 100
    else:
        progress = 0

    return {
        "speed_pages_per_hour": round(speed, 2),
        "progress_percent": round(progress, 2)
    }

