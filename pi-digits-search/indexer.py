import polars as pl
import sqlite3
import os
import sys

# Load words from CSV
words = pl.read_csv("words.csv", has_header=False, new_columns=["word"])


# Define optimized functions directly instead of importing
def ensure_pi_digits(num_digits=1000000):
    """Ensures we have a file with pi digits and returns the path."""
    pi_file = os.path.join(os.path.dirname(__file__), "pi_base32_1b.txt")
    if not os.path.exists(pi_file):
        sys.exit("pi_base32_1b.txt not found")
    return pi_file


def load_pi_digits(file_path, max_digits=None):
    """Load pi digits from a file, optionally limiting the number of digits."""
    with open(file_path, "r") as file:
        content = file.read().replace(".", "")
        return content[:max_digits] if max_digits else content


def ascii_to_base32(text):
    """Convert text to base32 representation with special character mapping."""
    mapping = {"!": "2", "?": "3", ",": "4", ".": "5", "-": "6", " ": "7"}
    formatted_text = text.upper()
    return "".join(mapping.get(c, c) for c in formatted_text)


def find_in_pi(search_string, pi_digits):
    """
    Find a string in pi digits, truncating if needed.
    Returns (position, found_string, is_exact_match) tuple.
    """
    original_length = len(search_string)

    # Try with full string first for efficiency
    pos = pi_digits.find(search_string)
    if pos != -1:
        return (pos, search_string, True)  # True indicates exact match

    # If not found, try with increasingly shorter substrings
    for length in range(original_length - 1, 1, -1):
        shorter_string = search_string[:length]
        pos = pi_digits.find(shorter_string)
        if pos != -1:
            return (pos, shorter_string, False)  # False indicates partial match

    return (-1, "", False)


# Create SQLite database connection
db_path = os.path.join(os.path.dirname(__file__), "pi_words.db")
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Create table if it doesn't exist - add is_exact_match column
cursor.execute(
    """
CREATE TABLE IF NOT EXISTS word_positions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    word TEXT NOT NULL,
    base32_representation TEXT NOT NULL,
    position INTEGER NOT NULL,
    found_length INTEGER NOT NULL,
    is_exact_match BOOLEAN NOT NULL
)
"""
)
conn.commit()

# Ensure we have pi digits and load them
pi_file = ensure_pi_digits()
pi_digits = load_pi_digits(pi_file)
print(f"Loaded {len(pi_digits)} digits of pi")

# Process each word and find its position in pi
total_words = len(words)
for i, row in enumerate(words.iter_rows(named=True)):
    word = row["word"]

    # Skip if word is empty or None
    if not word or word.isspace():
        continue

    # Convert to base32 representation
    base32_string = ascii_to_base32(word)

    print(
        f"Processing {i+1}/{total_words}: '{word}' (base32: {base32_string})\t\t\t\t", end="\r"
    )

    # Find position in pi digits
    position, found_string, is_exact_match = find_in_pi(base32_string, pi_digits)

    if position != -1:
        # Insert into database with is_exact_match flag
        cursor.execute(
            "INSERT INTO word_positions (word, base32_representation, position, found_length, is_exact_match) VALUES (?, ?, ?, ?, ?)",
            (word, base32_string, position, len(found_string), is_exact_match),
        )

        if (i + 1) % 100 == 0:  # Commit every 100 words
            conn.commit()
            print(f"Committed {i+1} words to database\n")
    else:
        print(f" Error: Could not find '{word}' in pi digits")

# Final commit
conn.commit()
print(f"Indexing complete. All {total_words} words processed.")

# Close connection
conn.close()
