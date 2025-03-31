import base64


def hex_to_base32(hex_string):
    # Remove '0x' prefix if present
    if hex_string.startswith("0x"):
        hex_string = hex_string[2:]

    # Make sure the hex string has an even number of characters
    if len(hex_string) % 2 != 0:
        hex_string = "0" + hex_string

    # Convert hex to bytes
    bytes_data = bytes.fromhex(hex_string)

    # Convert bytes to base32
    base32_result = base64.b32encode(bytes_data).decode("utf-8")

    return base32_result


def main():
    hex_input = "".join(open("pi_hex_1b.txt", "r").readlines()).replace(".", "")
    print(len(hex_input)," digits loaded")
    print(hex_input[:10])

    try:
        base32_result = hex_to_base32(hex_input)

        # Write result to file
        with open("base32.txt", "w") as file:
            file.write(base32_result)

        print(f"Base32 representation has been saved to 'base32.txt'")
        print(f"Digits in Base32 representation: {len(base32_result)}")

    except ValueError as e:
        print(f"Error: {e}")
        print("Please ensure you've entered a valid hexadecimal number.")


if __name__ == "__main__":
    main()
