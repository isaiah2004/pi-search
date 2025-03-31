import sqlite3

def search_words_in_db(search_string, db_path='database/pi_words.db'):
    """
    Searches for full words, partial matches, and character-wise matches in the pi_words database.
    Returns a dictionary with indexes of found words categorized by match type.
    """
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    # Prepare the result dictionary
    results = {
        'full_matches': [],
        'partial_matches': [],
        'character_matches': []
    }

    # Search for full words
    cursor.execute("SELECT id, word FROM words WHERE word = ?", (search_string,))
    full_matches = cursor.fetchall()
    results['full_matches'].extend(full_matches)

    # Search for partial matches
    cursor.execute("SELECT id, word FROM words WHERE word LIKE ?", ('%' + search_string + '%',))
    partial_matches = cursor.fetchall()
    results['partial_matches'].extend(partial_matches)

    # Search for character-wise matches
    cursor.execute("SELECT id, word FROM words")
    all_words = cursor.fetchall()
    for word in all_words:
        if all(char in word[1] for char in search_string):
            results['character_matches'].append(word)

    connection.close()
    return results


def find_indexes(search_string):
    """
    Converts the input string to Base32 and searches for words in the database.
    Returns the indexes of found words categorized by match type.
    """
    from utils.base32_converter import ascii_to_base32

    base32_string = ascii_to_base32(search_string)
    return search_words_in_db(base32_string)