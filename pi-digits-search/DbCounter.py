import sqlite3

def count_entries(db_path):
    """
    Removes all duplicate rows from the pi_words.db SQLite database.
    """
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        total_count = cursor.execute("SELECT COUNT(*) FROM word_positions").fetchone()[0]
        full_match_count = cursor.execute("SELECT COUNT(*) FROM word_positions WHERE is_exact_match = 1").fetchone()[0]
        
        print(f"Total entries: {total_count}")
        print(f"Full match entries: {full_match_count}")
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    finally:
        if conn:
            conn.close()

# Example usage
count_entries("pi_words.db")

