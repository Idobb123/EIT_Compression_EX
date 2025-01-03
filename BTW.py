import heapq
from collections import defaultdict


def suffix_array(input_string):
    n = len(input_string)
    suffix_arr = list(range(n))  # Initialize the suffix array as indices 0, 1, ..., n-1
    rank = [ord(c) for c in input_string] + [-1]  # Convert string characters to ranks (for comparison)
    tmp = [0] * (n + 1)

    k = 1
    while k < n:
        # Define a comparison function that compares suffixes based on their first k characters
        suffix_arr.sort(key=lambda x: (rank[x], rank[x + k] if x + k < n else -1))

        # Now, update the rank array to reflect the new sorting order
        tmp[suffix_arr[0]] = 0
        for i in range(1, n):
            tmp[suffix_arr[i]] = tmp[suffix_arr[i - 1]]
            if rank[suffix_arr[i]] != rank[suffix_arr[i - 1]] or \
                    (suffix_arr[i] + k < n and suffix_arr[i - 1] + k < n and rank[suffix_arr[i] + k] != rank[
                        suffix_arr[i - 1] + k]):
                tmp[suffix_arr[i]] += 1
        rank = tmp[:]
        k *= 2

    return suffix_arr


def burrows_wheeler_transform(input_string):
    # Step 1: Generate the suffix array
    suffix_arr = suffix_array(input_string)

    # Step 2: Extract the last column (from sorted suffixes)
    last_column = ''.join(input_string[(suffix + len(input_string) - 1) % len(input_string)] for suffix in suffix_arr)

    # Step 3: Find the position of the original string in the sorted list of suffixes
    original_position = suffix_arr.index(0)  # The original string's position is at the suffix starting at index 0

    return last_column, original_position


def move_to_front(input_string):
    """Move-to-Front Transformation"""
    alphabet = list(set(input_string))  # Alphabet of unique characters
    output = []
    for char in input_string:
        index = alphabet.index(char)
        output.append(index)  # Append the position of the character in the alphabet
        alphabet.insert(0, alphabet.pop(index))  # Move this character to the front
    return output


def run_length_encoding(input_list):
    """Run-Length Encoding"""
    encoded = []
    count = 1
    for i in range(1, len(input_list)):
        if input_list[i] == input_list[i - 1]:
            count += 1
        else:
            encoded.append((input_list[i - 1], count))
            count = 1
    encoded.append((input_list[-1], count))  # Append the last run
    return encoded


def huffman_coding(input_list):
    """Huffman Coding"""
    freq = defaultdict(int)
    for symbol in input_list:
        freq[symbol] += 1

    # Create a heap of the frequency table
    heap = [[weight, [symbol, ""]] for symbol, weight in freq.items()]
    heapq.heapify(heap)

    while len(heap) > 1:
        lo = heapq.heappop(heap)
        hi = heapq.heappop(heap)
        for pair in lo[1:]:
            pair[1] = '0' + pair[1]
        for pair in hi[1:]:
            pair[1] = '1' + pair[1]
        heapq.heappush(heap, [lo[0] + hi[0]] + lo[1:] + hi[1:])

    # Generate the Huffman codes
    huff_codes = {}
    for pair in heap[0][1:]:
        huff_codes[pair[0]] = pair[1]

    # Encode the input using the Huffman codes
    encoded_output = ''.join([huff_codes[symbol] for symbol in input_list])
    return encoded_output, huff_codes


def compress_file(file_path):
    # Step 1: Read the file
    with open(file_path, 'rb') as file:
        data = file.read()

    # Convert binary data to a string (if it's text-based)
    input_string = ''.join(format(byte, '08b') for byte in data)  # Convert bytes to binary string

    # Step 2: Apply BWT
    bwt_result, original_position = burrows_wheeler_transform(input_string)

    # Step 3: Apply Move-to-Front Transformation
    mtf_result = move_to_front(bwt_result)

    # Step 4: Apply Run-Length Encoding
    rle_result = run_length_encoding(mtf_result)

    # Step 5: Apply Huffman Coding
    huffman_encoded, huffman_codes = huffman_coding(
        [item for sublist in rle_result for item in sublist])  # Flatten the RLE result

    # Save the compressed data to a file
    with open(f"{file_path}.compressed", 'wb') as compressed_file:
        # Save Huffman codes and the compressed bitstream
        compressed_file.write(bytes(huffman_encoded, 'utf-8'))

    print(f"File {file_path} compressed successfully to {file_path}.compressed")
    return huffman_encoded, huffman_codes


# Example usage
file_path = "Samp1.bin"  # Change this to the path of the file you want to compress
compressed_data, huffman_codes = compress_file(file_path)
print("Huffman Codes:", huffman_codes)
