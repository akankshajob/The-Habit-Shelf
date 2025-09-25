from flask import Blueprint, request, jsonify
from .models import UserLog
from . import db
from datetime import datetime

main = Blueprint('main', __name__)

@main.route('/')
def home():
    return "📚 Welcome to The Habit Shelf Flask App!"

@main.route('/add_log', methods=['POST'])
def add_log():
    data = request.json
    new_log = UserLog(
        date=datetime.today().strftime("%Y-%m-%d"),
        book_name=data['book_name'],
        pages_read=data['pages_read'],
        reading_time_minutes=data['reading_time_minutes']
    )
    db.session.add(new_log)
    db.session.commit()
    return jsonify({"message": "User log added successfully!"})
from .utils import fetch_book_metadata
from .models import BookMetadata

@main.route('/fetch_metadata', methods=['POST'])
def get_metadata():
    data = request.json
    book_name = data.get('book_name')
    
    metadata = fetch_book_metadata(book_name)
    if not metadata:
        return jsonify({"message": "Book not found"}), 404
    
    # Save metadata to DB if not exists
    existing = BookMetadata.query.filter_by(title=metadata['title']).first()
    if not existing:
        new_book = BookMetadata(
            title=metadata['title'],
            author=metadata['author'],
            genre=metadata['genre'],
            total_pages=metadata['total_pages']
        )
        db.session.add(new_book)
        db.session.commit()
    
    return jsonify(metadata)
from .models import ProcessedLog

@main.route('/process_log', methods=['POST'])
def process_log():
    data = request.json
    book_name = data['book_name']
    pages_read = data['pages_read']
    reading_time_minutes = data['reading_time_minutes']

    # Get total pages from BookMetadata if exists
    book = BookMetadata.query.filter_by(title=book_name).first()
    total_pages = book.total_pages if book else 0

    metrics = calculate_metrics(pages_read, reading_time_minutes, total_pages)

    # Save processed log
    processed = ProcessedLog(
        date=data.get('date', ""),
        book_name=book_name,
        pages_read=pages_read,
        reading_time_minutes=reading_time_minutes,
        speed_pages_per_hour=metrics['speed_pages_per_hour'],
        progress_percent=metrics['progress_percent']
    )
    db.session.add(processed)
    db.session.commit()

    return jsonify({"message": "Log processed", "metrics": metrics})

