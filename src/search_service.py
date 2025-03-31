import os
import sqlite3

# for dev
# from utils.base32_converter import ascii_to_base32

from .utils.base32_converter import ascii_to_base32
import logging
import pprint as p

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def search_word_with_conn(cursor, base32_string):
    """
    Helper function to search for a word using an existing database cursor.
    Returns only the first match found.
    """
    cursor.execute("SELECT * FROM word_positions WHERE word = ?", (base32_string,))
    result = cursor.fetchone()
    logger.info(f"Found match: {result}")
    return result if result else []


def search_partial_word_with_conn(cursor, base32_string):
    """
    Helper function to search for partial word matches using an existing database cursor.
    Returns matches that start with the given string, ordered by length (longest first).
    """
    cursor.execute(
        "SELECT * FROM word_positions WHERE word  LIKE ? and is_exact_match = 1 ORDER BY length(word) DESC LIMIT 3",
        (base32_string + "%",),
    )
    results = cursor.fetchall()
    logger.info(f"{results} partial matches for: {base32_string}")

    return results if results else []



def process_search_request(input_string, db_path="database/pi_words.db"):
    """
    Process the input string and return search results.
    Only searches for full matches.
    """
    if not input_string:
        return {"error": "Input string cannot be empty."}

    # Split the input string into words
    words = input_string.split()
    found_matches = []

    # Open a single database connection for ALL searches
    conn = None
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Process each word separately
        for word in words:
            word = word.lower()
            # Get full match using the existing cursor directly
            base32_word = ascii_to_base32(word)
            logger.info(f"processing: {word}, b32: {base32_word}")
            match = search_word_with_conn(cursor, word)

            # If we found a match, add it to our results

            if len(match) > 1 and match[4] == len(word):
                logger.info(f"full match for: {word}")
                found_matches.append(match)
            else:
                if len(match) > 1:
                    logger.info(
                        f"no indexed full match for: {word} breaking into components {word[:match[4]]} , {word[match[4]:]}"
                    )
                    # Find the best way to construct the word from segments
                    compositeMatches = []
                    compositeMatches.append(match)
                    resolvedSubString = word[:match[4]]
                    unresolvedSubString = word[match[4]:]
                    for i in unresolvedSubString:
                        compositeMatches.append(search_word_with_conn(cursor, i))
                    logger.info(f"- composite matches: {compositeMatches}")
                    found_matches.append(compositeMatches)
                else:
                    logger.info(f"no match for: {word}, breaking into segments")
                    compositeMatches = []
                    resolvedSubString = ""
                    r_match=[]
                    for i in range(1,len(word)):
                        print(f"========{i}========={word[:i]}========")
                        op_match = search_word_with_conn(cursor, word[:i])
                        if len(op_match) > 1 and op_match[4] == len(word[:i]):
                            r_match=op_match
                            print(r_match)
                            resolvedSubString = word[:i]

                    compositeMatches.append(r_match)
                    unresolvedSubString = word[len(resolvedSubString):]
                    for i in unresolvedSubString:
                        compositeMatches.append(search_word_with_conn(cursor, i))
                    found_matches.append(compositeMatches)

        logger.info(f"results: {found_matches}")

    except sqlite3.Error as e:
        logger.error(f"Database error: {e}")
        return {"error": f"Database error: {str(e)}"}
    finally:
        # Ensure connection is closed even if an exception occurs
        if conn:
            conn.close()

    # Return a response with the matches found
    return found_matches


if __name__ == "__main__":
    p.pprint(process_search_request("Hello I am PI"))
