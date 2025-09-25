import sqlite3
import os

DB_FILE = os.path.join("data", "reading_habits.db")

def create_connection():
    return sqlite3.connect(DB_FILE)
    
def init_db():
    conn = create_connection()
    cursor = conn.cursor()
    
    # User logs table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            book_name TEXT NOT NULL,
            pages_read INTEGER NOT NULL,
            reading_time_minutes INTEGER NOT NULL
        )
    ''')

    # Book metadata table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS book_metadata (
            book_id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT,
            genre TEXT,
            total_pages INTEGER
        )
    ''')

    # Processed metrics table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS processed_logs (
            log_id INTEGER PRIMARY KEY,
            date TEXT,
            book_name TEXT,
            pages_read INTEGER,
            reading_time_minutes INTEGER,
            speed_pages_per_hour REAL,
            progress_percent REAL
        )
    ''')

    conn.commit()
    conn.close()
    print("✅ Database initialized at", DB_FILE)

if __name__ == "__main__":
    init_db()
