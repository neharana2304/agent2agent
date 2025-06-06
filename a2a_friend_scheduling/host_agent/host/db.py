import os
import sqlite3

DB_FILE = "pickleball_reservations.db"


def get_db_connection():
    """Establishes a connection to the SQLite database."""
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn


def initialize_database():
    """Initializes the database and creates the reservations table if it doesn't exist."""
    if os.path.exists(DB_FILE):
        print("Database already exists.")
        return

    print("Initializing new database...")
    conn = get_db_connection()
    cursor = conn.cursor()

    # Create reservations table
    cursor.execute(
        """
        CREATE TABLE reservations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            reservation_datetime TEXT NOT NULL,
            friend_names TEXT NOT NULL,
            court_id INTEGER NOT NULL
        )
    """
    )

    conn.commit()
    conn.close()
    print("Database initialized successfully.")


if __name__ == "__main__":
    initialize_database()
