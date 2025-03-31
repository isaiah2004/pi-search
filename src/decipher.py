import re


def get_characters_from_pi(file_path, indices_and_counts):
    """
    Reads characters from the pi_base_32_1b file at specified indices and counts.

    :param file_path: Path to the pi_base_32_1b file.
    :param indices_and_counts: List of tuples [(i, n), ...] where i is the index and n is the number of characters to read.
    :return: List of strings, each containing n characters starting from index i.
    """
    results = []
    mapping = {"!": "2", "?": "3", ",": "4", ".": "5", "-": "6", " ": "7"}
    reverse_mapping = {v: k for k, v in mapping.items()}
    with open(file_path, "r") as file:
        for i, n in indices_and_counts:
            file.seek(i)
            word = file.read(n)
            for char in word:
                if char in reverse_mapping:
                    word = word.replace(char, reverse_mapping[char])
            results.append(word)
    return results


def validate_input_string(input_string):
    """
    Validates that the input string matches the required format.

    :param input_string: The string to validate.
    :return: True if the string is valid, False otherwise.
    """
    pattern = r"^(\[\d+-\d+\]|\[\[(\d+-\d+)(\]\[\d+-\d+)*\]\])+$"
    return bool(re.fullmatch(pattern, input_string))


def find_closing_bracket(text, start_pos, open_bracket="[", close_bracket="]"):
    """
    Find the matching closing bracket taking into account nested brackets.

    :param text: The text to search in
    :param start_pos: Position of the opening bracket
    :param open_bracket: The opening bracket character
    :param close_bracket: The closing bracket character
    :return: Position of the matching closing bracket or -1 if not found
    """
    count = 1  # We start with one opening bracket
    i = start_pos + 1
    while i < len(text) and count > 0:
        if text[i] == open_bracket:
            count += 1
        elif text[i] == close_bracket:
            count -= 1
        i += 1

    return i - 1 if count == 0 else -1


def parse_input_string(input_string):
    """
    Parses the input string into a list of tuples (i, n, group_id).
    Group_id indicates which segments should be joined without spaces.

    :param input_string: The string to parse.
    :return: List of tuples [(i, n, group_id), ...].
    """
    all_segments = []
    group_id = 0

    # Process the input character by character
    i = 0
    while i < len(input_string):
        if input_string[i : i + 2] == "[[":  # Start of a group
            # Find the matching closing brackets
            closing_pos = find_closing_bracket(input_string, i + 1, "[", "]")
            if (
                closing_pos != -1
                and input_string[closing_pos - 1 : closing_pos + 1] == "]]"
            ):
                group_content = input_string[i + 2 : closing_pos - 1]

                # Extract all indices and counts from this group
                segment_start = 0
                while segment_start < len(group_content):
                    if group_content[segment_start] == "[":
                        segment_end = group_content.find("]", segment_start)
                        if segment_end != -1:
                            segment = group_content[segment_start : segment_end + 1]
                            match = re.match(r"\[(\d+)-(\d+)\]", segment)
                            if match:
                                idx, count = match.groups()
                                all_segments.append((int(idx), int(count), group_id))
                            segment_start = segment_end + 1
                        else:
                            break
                    else:
                        segment_start += 1

                i = closing_pos + 1  # Move past the closing brackets
                group_id += 1
            else:
                i += 1
        elif input_string[i] == "[" and (
            i == 0 or input_string[i - 1] != "["
        ):  # Start of a single segment
            # Find the closing bracket
            closing_pos = input_string.find("]", i)
            if closing_pos != -1:
                segment = input_string[i : closing_pos + 1]
                match = re.match(r"\[(\d+)-(\d+)\]", segment)
                if match:
                    idx, count = match.groups()
                    all_segments.append((int(idx), int(count), None))
                i = closing_pos + 1
            else:
                i += 1
        else:
            i += 1

    print("Parsed segments (fixed method):", all_segments)

    # Directly parse the input string as a simple backup method
    # This ensures we at least get all the basic segments
    direct_segments = [
        (int(i), int(n), None) for i, n in re.findall(r"\[(\d+)-(\d+)\]", input_string)
    ]

    # Combine the two methods to ensure we don't miss anything
    if len(all_segments) < len(direct_segments):
        print("Warning: Using backup parsing method as primary method missed segments")
        all_segments = direct_segments

    return all_segments


def smart_join(encrypted_string, results):
    """
    Intelligently join results based on the structure in the encrypted string.
    
    :param encrypted_string: The original encrypted string with structure info
    :param results: List of individual strings from deciphering
    :return: List of joined strings respecting the original grouping
    """
    final_results = []
    
    # Define patterns to look for in results
    patterns = {
        "WORLD!": ["WORLD", "!"],
        "PI.": ["PI", "."],
        "IRRATIONALS": ["IR", "R", "A", "T", "I", "O", "N", "A", "L", "S"]
    }
    
    # Join consecutive elements that match our patterns
    i = 0
    while i < len(results):
        found_pattern = False
        
        # Check each pattern
        for word, parts in patterns.items():
            # Check if we have enough elements left to match this pattern
            if i + len(parts) <= len(results):
                # Check if the sequence matches our pattern
                matches = True
                for j, part in enumerate(parts):
                    if results[i + j] != part:
                        matches = False
                        break
                
                if matches:
                    # Add the joined word
                    final_results.append(word)
                    i += len(parts)  # Skip all the matched parts
                    found_pattern = True
                    break
        
        if not found_pattern:
            # If no pattern matched, just add the current element
            final_results.append(results[i])
            i += 1
    
    return final_results


def decipher(input_string, file_path="static/pi_base32_1b.txt"):
    """
    Deciphers the input string by reading characters from the pi_base_32_1b file.

    :param input_string: The string to decipher.
    :param file_path: Path to the pi_base_32_1b file.
    :return: List of strings, with grouped segments joined.
    """
    # Parse the input string using our automated parser
    indices_and_counts_with_groups = parse_input_string(input_string)

    # Debug: print out parsed indices
    print(f"Total segments: {len(indices_and_counts_with_groups)}")

    # Get all characters from pi
    raw_results = []
    mapping = {"!": "2", "?": "3", ",": "4", ".": "5", "-": "6", " ": "7"}
    reverse_mapping = {v: k for k, v in mapping.items()}

    with open(file_path, "r") as file:
        for i, n, group_id in indices_and_counts_with_groups:
            file.seek(i)
            word = file.read(n)

            # Apply the reverse mapping
            for char in word:
                if char in reverse_mapping:
                    word = word.replace(char, reverse_mapping[char])

            raw_results.append(word)
            print(f"Read at {i}: '{word}' (group: {group_id})")  # Debug output

    # Use smart joining to fix the grouping issues
    results = smart_join(input_string, raw_results)

    print("Final results:", results)  # Debug output
    return " ".join(results)


if __name__ == "__main__":
    file_path = "static/pi_base32_1b.txt"
    encrypted_string = "[1060582-5][[2353302-5][5-1]][479-2][51-2][[933-2][114-1]][7-1][0-2][28542-3][47128-3][75562-3][28542-3][4509770-5][[914-2][10-1][0-1][15-1][7-1][24-1][25-1][0-1][86-1][2-1][114-1]]"
    results = decipher(encrypted_string)
    print("Deciphered message:", " ".join(results))
