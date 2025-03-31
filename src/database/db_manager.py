import sqlite3

class DBManager:
    def __init__(self, db_path):
        self.db_path = db_path
        self.connection = None

    def connect(self):
        """Establish a database connection."""
        if self.connection is None:
            self.connection = sqlite3.connect(self.db_path)
            self.connection.row_factory = sqlite3.Row

    def close(self):
        """Close the database connection."""
        if self.connection:
            self.connection.close()
            self.connection = None

    def get_words(self):
        """Retrieve all words from the database."""
        self.connect()
        cursor = self.connection.cursor()
        cursor.execute("SELECT word FROM words")
        words = cursor.fetchall()
        return [row['word'] for row in words]

    def find_full_matches(self, search_string):
        """Find full matches for the search string."""
        self.connect()
        cursor = self.connection.cursor()
        cursor.execute("SELECT word FROM words WHERE word = ?", (search_string,))
        return [row['word'] for row in cursor.fetchall()]

    def find_partial_matches(self, search_string):
        """Find partial matches for the search string."""
        self.connect()
        cursor = self.connection.cursor()
        cursor.execute("SELECT word FROM words WHERE word LIKE ?", ('%' + search_string + '%',))
        return [row['word'] for row in cursor.fetchall()]

    def find_character_matches(self, search_string):
        """Find character-wise matches for the search string."""
        self.connect()
        cursor = self.connection.cursor()
        cursor.execute("SELECT word FROM words WHERE word LIKE ?", ('%' + ''.join(search_string) + '%',))
        return [row['word'] for row in cursor.fetchall()]

    def __del__(self):
        self.close()