import heapq
import os
import pickle
from collections import defaultdict


# Build the Huffman tree
class HuffmanNode:
    def __init__(self, char=None, freq=None):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq


def build_huffman_tree(data):
    frequency = defaultdict(int)
    for byte in data:
        frequency[byte] += 1

    # Create a priority queue (min-heap) with all the frequency nodes
    priority_queue = [HuffmanNode(char=char, freq=freq) for char, freq in frequency.items()]
    heapq.heapify(priority_queue)

    # Build the Huffman tree
    while len(priority_queue) > 1:
        left = heapq.heappop(priority_queue)
        right = heapq.heappop(priority_queue)

        merged = HuffmanNode(freq=left.freq + right.freq)
        merged.left = left
        merged.right = right

        heapq.heappush(priority_queue, merged)

    return priority_queue[0]


# Generate Huffman Codes from the Tree
def generate_huffman_codes(node, current_code="", codes=defaultdict()):
    if node is None:
        return

    # If this is a leaf node, save the code
    if node.char is not None:
        codes[node.char] = current_code

    # Traverse left and right
    generate_huffman_codes(node.left, current_code + "0", codes)
    generate_huffman_codes(node.right, current_code + "1", codes)

    return codes


# Encode the Data Using Huffman Codes
def encode_data(data, huffman_codes):
    return ''.join(huffman_codes[byte] for byte in data)


# Step 1: Compression (Storing the Dictionary)
def huffman_compress(input_file_path, output_file_path):
    with open(input_file_path, 'rb') as f:
        data = f.read()

    # Build the Huffman Tree
    root = build_huffman_tree(data)

    # Generate Huffman codes
    huffman_codes = generate_huffman_codes(root)

    # Encode the data
    encoded_data = encode_data(data, huffman_codes)

    # Write the dictionary (mapping of character -> Huffman code) and encoded data to the output file
    with open(output_file_path, 'wb') as f:
        # Write the length of the dictionary first
        f.write(len(huffman_codes).to_bytes(4, 'big'))

        # Write the dictionary
        for char, code in huffman_codes.items():
            f.write(char.to_bytes(1, 'big'))  # Write the character
            f.write(len(code).to_bytes(1, 'big'))  # Write the length of the code
            f.write(int(code, 2).to_bytes((len(code) + 7) // 8, 'big'))  # Write the Huffman code

        # Write the encoded data
        f.write(int(encoded_data, 2).to_bytes((len(encoded_data) + 7) // 8, 'big'))

    print(f"Compressed data written to {output_file_path}")


# Step 2: Decompression (Restoring the Original Data)
def huffman_decompress(input_file_path, output_file_path):
    with open(input_file_path, 'rb') as f:
        # Read the length of the dictionary
        dict_size = int.from_bytes(f.read(4), 'big')

        # Read the dictionary
        huffman_codes = {}
        for _ in range(dict_size):
            char = int.from_bytes(f.read(1), 'big')
            code_length = int.from_bytes(f.read(1), 'big')
            code_bits = f.read((code_length + 7) // 8)
            code = bin(int.from_bytes(code_bits, 'big'))[2:].zfill(code_length)  # Convert to binary string
            huffman_codes[code] = char

        # Rebuild the Huffman tree from the codes
        decoding_tree = {}
        for code, char in huffman_codes.items():
            decoding_tree[code] = chr(char)

        # Read the encoded data
        encoded_data = f.read()

        # Decode the encoded data
        bit_str = ''.join([bin(byte)[2:].zfill(8) for byte in encoded_data])
        decoded_data = ""
        current_code = ""
        for bit in bit_str:
            current_code += bit
            if current_code in decoding_tree:
                decoded_data += decoding_tree[current_code]
                current_code = ""

    # Write the decoded data to the output file
    with open(output_file_path, 'wb') as f:
        f.write(decoded_data.encode('utf-8'))  # Write the decoded content back as a binary file

    print(f"Decompressed data written to {output_file_path}")


if __name__ == "__main__":
    # Example usage
    input_file = "Samp1.bin"  # The file you want to compress
    compressed_file = "compressed.bin"
    decompressed_file = "decompressed.bin"

    # Compression step
    huffman_compress(input_file, compressed_file)

    # Decompression step
    huffman_decompress(compressed_file, decompressed_file)
