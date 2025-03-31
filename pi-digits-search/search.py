import os
import urllib.request


def ensure_pi_digits(num_digits=1000000):
    """
    Ensures we have a file with at least the specified number of pi digits.
    Returns the path to the file.
    """
    pi_file = os.path.join(os.path.dirname(__file__), "pi_base32_1b.txt")

    if not os.path.exists(pi_file):
        sys.exit("pi_base32_1b.txt not found")

    return pi_file


def load_pi_digits(file_path, max_digits=None):
    """
    Load pi digits from a file, skipping the decimal point.
    """
    with open(file_path, "r") as file:
        content = file.read().replace(".", "")  # Remove decimal point
        return content[:max_digits] if max_digits else content


def ascii_to_base32(text):
    # Convert string to bytes, then to base32, then back to string
    mapping = { "!": "2", "?": "3", ",": "4", ".": "5", "-": "6"," ": "7"}
    formatted_text = text.upper()
    formatted_text = "".join(mapping.get(c, c) for c in formatted_text)
    return formatted_text


def find_in_pi(search_string, pi_digits):
    """
    Find a string in pi digits.
    Returns the position (0-indexed) where the string starts in pi digits.
    Returns -1 if not found.
    """
    idx = len(search_string)
    print(f"Searching for {search_string}")
    print(pi_digits[:10])
    pos = -1

    while idx > 1:
        pos = pi_digits.find(search_string)
        if pos == -1:
            print(
                f"{search_string} - Not found, trying again with one less character: {search_string[:-1]}"
            )
            search_string = search_string[:-1]
            idx -= 1
        else:
            return (pos,search_string)

    return (pos,search_string)


def main():
    """
    Main function to search for ASCII strings in pi digits.
    """
    try:
        # Ensure we have pi digits and load them
        pi_file = ensure_pi_digits()
        pi_digits = load_pi_digits(pi_file)

        print(f"Loaded {len(pi_digits)} digits of pi")

        while True:
            search_string = input(
                "\nEnter string to search for in pi_b32 (or 'qqq' to quit): "
            )
            if search_string.lower() == "qqq":
                break

            base32_string = ascii_to_base32(search_string)
            print(f"Searching for base32 representation: {base32_string}")

            print("-x-")
            position,search_string = find_in_pi(base32_string, pi_digits)
            print("-x-")

            if position != -1:
                print(f"Found '{search_string}' at position {position} in pi digits")
                # Get the actual matched substring with the correct case
                matched_substring = pi_digits[position : position + len(search_string)]
                print(
                    f"Context: ...{pi_digits[max(0, position-10):position]}<{matched_substring}>..."
                )
            else:
                print(f"'{search_string}' was not found in the loaded pi digits")

    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
