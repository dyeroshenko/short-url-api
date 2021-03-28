import sqlite3

class Database:
    '''
    Enters or initializes (if not created yet: see [init_db] method) SQLite DB.
    '''
    def __init__(self, db: str) -> None:
        self.db = db
        self.init_db()

    def init_db(self) -> None:
        with self as cursor:
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS urls (
                id INTEGER PRIMARY KEY,
                hashed_id TEXT NOT NULL,
                timestamp_CET TEXT NOT NULL,
                full_url TEXT NOT NULL, 
                domain TEXT NOT NULL,
                visits INTEGER NOT NULL
                )
            """)

    def __enter__(self) -> None:
        self.connector = sqlite3.connect(self.db)
        self.cursor = self.connector.cursor()
        return self.cursor

    def __exit__(self, exc_type, exc_val, exc_trace) -> None:
        self.connector.commit()
        self.connector.close()