from . import db

class UserLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(20), nullable=False)
    book_name = db.Column(db.String(200), nullable=False)
    pages_read = db.Column(db.Integer, nullable=False)
    reading_time_minutes = db.Column(db.Integer, nullable=False)

class BookMetadata(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    author = db.Column(db.String(100))
    genre = db.Column(db.String(50))
    total_pages = db.Column(db.Integer)

class ProcessedLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(20))
    book_name = db.Column(db.String(200))
    pages_read = db.Column(db.Integer)
    reading_time_minutes = db.Column(db.Integer)
    speed_pages_per_hour = db.Column(db.Float)
    progress_percent = db.Column(db.Float)
