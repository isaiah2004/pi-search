def count_hex_digits(file_path):
    try:
        hex_chars = set('0123456789ABCDEFabcdef')
        count = 0
        with open(file_path, 'r') as file:
            for line in file:
                count += sum(1 for c in line if c in hex_chars)
        return count
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return 0

if __name__ == "__main__":
    file_path = "./pi_hex_1b.txt"  # Replace with the actual file path
    count = count_hex_digits(file_path)
    print(f"Total hexadecimal digits in the file: {count}")