import os
import csv
import sqlite3
from datetime import datetime
from database import create_connection, init_db
from utils import fetch_book_metadata

# Initialize DB
init_db()

DB_FILE = os.path.join("data", "reading_habits.db")

# --- Phase 1: User Log Ingestion ---
def ingest_user_log(book_name, pages_read, reading_time_minutes):
    date_today = datetime.today().strftime("%Y-%m-%d")
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO user_logs (date, book_name, pages_read, reading_time_minutes) VALUES (?, ?, ?, ?)",
                   (date_today, book_name, pages_read, reading_time_minutes))
    conn.commit()
    conn.close()
    print(f"✅ User log added for '{book_name}'")

# --- Phase 2: Fetch Book Metadata ---
def add_book_metadata(book_name):
    metadata = fetch_book_metadata(book_name)
    if metadata:
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO book_metadata (title, author, genre, total_pages) VALUES (?, ?, ?, ?)",
                       (metadata['title'], metadata['author'], metadata['genre'], metadata['total_pages']))
        conn.commit()
        conn.close()
        print(f"✅ Metadata added for '{book_name}'")
    else:
        print(f"⚠️ Metadata not found for '{book_name}'")

# --- Phase 3: Transform & Calculate Metrics ---
def process_metrics():
    conn = create_connection()
    cursor = conn.cursor()
    
    # Join user_logs with book_metadata
    cursor.execute('''
        SELECT u.id, u.date, u.book_name, u.pages_read, u.reading_time_minutes, b.total_pages
        FROM user_logs u
        LEFT JOIN book_metadata b
        ON u.book_name = b.title
    ''')
    logs = cursor.fetchall()
    
    for log in logs:
        log_id, date, book_name, pages_read, reading_time, total_pages = log
        if reading_time == 0:
            speed = 0
        else:
            speed = pages_read / (reading_time / 60)  # pages/hour
        progress = 0 if not total_pages else (pages_read / total_pages) * 100
        
        # Insert into processed_logs
        cursor.execute('''
            INSERT OR REPLACE INTO processed_logs 
            (log_id, date, book_name, pages_read, reading_time_minutes, speed_pages_per_hour, progress_percent)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (log_id, date, book_name, pages_read, reading_time, speed, progress))
    
    conn.commit()
    conn.close()
    print("✅ Metrics processed and stored in DB")

# --- Phase 4: View Processed Logs ---
def view_processed_logs():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM processed_logs ORDER BY date DESC")
    rows = cursor.fetchall()
    for row in rows:
        print(row)
    conn.close()

# --- CLI Menu ---
def main():
    while True:
        print("\n📚 The Habit Shelf - ETL Menu")
        print("1. Add User Log")
        print("2. Add Book Metadata")
        print("3. Process Metrics")
        print("4. View Processed Logs")
        print("5. Exit")
        choice = input("Enter choice: ")

        if choice == "1":
            book = input("Book name: ")
            pages = int(input("Pages read: "))
            time_min = int(input("Reading time in minutes: "))
            ingest_user_log(book, pages, time_min)
        elif choice == "2":
            book = input("Book name to fetch metadata: ")
            add_book_metadata(book)
        elif choice == "3":
            process_metrics()
        elif choice == "4":
            view_processed_logs()
        elif choice == "5":
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice. Try again.")

if __name__ == "__main__":
    main()
