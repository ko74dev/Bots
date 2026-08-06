# db.py
import sqlite3
from typing import List, Dict, Any

DATABASE_PATH = "salon.db"

def get_connection() -> sqlite3.Connection:
    """Returns a connection to the SQLite database."""
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def _ensure_table_exists(cursor):
    """Ensure the services table exists."""
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS services (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            price TEXT NOT NULL
        )
    ''')

def init_db():
    """Initialize the database with necessary tables."""
    conn = get_connection()
    cursor = conn.cursor()
    _ensure_table_exists(cursor)
    # Insert default services if not exist
    default_services = [
        ("Стрижка", "2 500 ₽"),
        ("Маникюр", "1 800 ₽"),
        ("Макияж", "3 000 ₽"),
        ("Педикюр", "2 200 ₽"),
    ]
    for name, price in default_services:
        cursor.execute('''
            INSERT OR IGNORE INTO services (name, price) VALUES (?, ?)
        ''', (name, price))
    conn.commit()
    conn.close()

def get_all_services() -> List[Dict[str, str]]:
    """Retrieve all services from the database."""
    conn = get_connection()
    cursor = conn.cursor()
    _ensure_table_exists(cursor)
    cursor.execute('SELECT name, price FROM services')
    rows = cursor.fetchall()
    services = [{'name': row['name'], 'price': row['price']} for row in rows]
    conn.close()
    return services
