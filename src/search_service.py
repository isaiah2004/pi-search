import os
import sqlite3
from .utils.base32_converter import ascii_to_base32

def search_words_in_db(search_string, db_path='database/pi_words.db'):
    """
    Searches for full words, partial matches, and character-wise matches in the database.
    Returns a dictionary with indexes of found words.
    """
    base32_string = ascii_to_base32(search_string)
    results = {
        'full_matches': [],
        'partial_matches': [],
        'character_matches': []
    }

    # Connect to the database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Query for full matches
    cursor.execute("SELECT id FROM words WHERE word = ?", (base32_string,))
    results['full_matches'] = [row[0] for row in cursor.fetchall()]

    # Query for partial matches
    cursor.execute("SELECT id FROM words WHERE word LIKE ?", ('%' + base32_string + '%',))
    results['partial_matches'] = [row[0] for row in cursor.fetchall()]

    # Query for character-wise matches
    cursor.execute("SELECT id FROM words WHERE word LIKE ?", ('%' + ''.join(base32_string) + '%',))
    results['character_matches'] = [row[0] for row in cursor.fetchall()]

    # Close the database connection
    conn.close()

    return results


def process_search_request(input_string):
    """
    Process the input string and return search results.
    """
    if not input_string:
        return {"error": "Input string cannot be empty."}

    search_results = search_words_in_db(input_string)
    return search_results