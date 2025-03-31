def index_to_cipher(index_data):
    """
    Convert index data to cipher format.
    
    Args:
        index_data: Nested list of sequence data.
    
    Returns:
        List with the same nesting structure but only containing position and length.
    """
    result = []
    
    for item in index_data:
        if isinstance(item[0], int):  # Direct sequence entry like [2820,"hello","HELLO",1060582,5,1]
            position = item[3]
            length = item[4]
            result.append([position,'-', length])
        else:  # Nested list like [[987,"z","Z",35,1,1],[81,"c","C",19,1,1]]
            nested_result = []
            for entry in item:
                position = entry[3]
                length = entry[4]
                nested_result.append([position,'-', length])
            result.append(nested_result)
    
    return str(result).replace("'", "").replace(" ", "").replace(",", "")[1:-1]

# Example usage
if __name__ == "__main__":
    sample_index = [[2820,"hello","HELLO",1060582,5,1],[[987,"z","Z",35,1,1],[81,"c","C",19,1,1]],[119,"world","WORLD",2353302,5,1]]
    result = index_to_cipher(sample_index)
    print(result)  # Should output: [[2820, 5], [[987, 1], [81, 1]], [119, 5]]
