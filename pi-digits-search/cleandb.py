import sqlite3

def remove_duplicates_from_db(db_path):
    """
    Removes all duplicate rows from the pi_words.db SQLite database.
    """
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Create a temporary table with unique rows
        cursor.execute("""
            CREATE TABLE temp_table AS
            SELECT * FROM word_positions
            WHERE rowid IN (
            SELECT MIN(rowid)
            FROM word_positions
            GROUP BY word
            );
        """)

        # Drop the original table
        cursor.execute("DROP TABLE word_positions;")

        # Rename the temporary table to the original table name
        cursor.execute("ALTER TABLE temp_table RENAME TO word_positions;")
        # cursor.execute("DROP TABLE SQLITE_SEQUENCE ;")
        
        # cursor.execute("CREATE TABLE SQLITE_SEQUENCE ;")
        cursor.execute("DELETE FROM SQLITE_SEQUENCE WHERE name='word_positions';")
        cursor.execute("INSERT INTO SQLITE_SEQUENCE (name, seq) VALUES ('word_positions', (SELECT COUNT(*) FROM word_positions));")
        conn.commit()
        print("Duplicates removed successfully.")
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    finally:
        if conn:
            conn.close()

# Example usage
remove_duplicates_from_db("pi_words.db")

