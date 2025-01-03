import os
import time


def lz78_compress(input_file_path, output_file_path):
    """Compress a file using the LZ78 algorithm."""
    with open(input_file_path, 'rb') as f:
        data = f.read()

    dictionary = {}
    next_code = 1
    current_string = b""
    compressed_data = []

    for byte in data:
        current_string += bytes([byte])
        if current_string not in dictionary:
            dictionary[current_string] = next_code
            next_code += 1
            # Output (index, character)
            if len(current_string) == 1:
                compressed_data.append((0, byte))  # No previous string, index 0
            else:
                prefix = current_string[:-1]
                compressed_data.append((dictionary[prefix], byte))
            current_string = b""

    if current_string:
        prefix = current_string[:-1]
        compressed_data.append((dictionary.get(prefix, 0), current_string[-1]))

    # Write the compressed data to a file
    with open(output_file_path, 'wb') as f:
        for index, byte in compressed_data:
            f.write(index.to_bytes(2, 'big'))  # Write index (2 bytes)
            f.write(bytes([byte]))  # Write the next character


def lz78_decompress(input_file_path, output_file_path):
    """Decompress a file using the LZ78 algorithm."""
    with open(input_file_path, 'rb') as f:
        compressed_data = []
        while True:
            index_bytes = f.read(2)
            if not index_bytes:
                break
            index = int.from_bytes(index_bytes, 'big')
            byte = f.read(1)
            if not byte:
                break
            compressed_data.append((index, byte[0]))

    dictionary = {}
    next_code = 1
    decompressed_data = bytearray()

    for index, byte in compressed_data:
        if index == 0:
            current_string = bytes([byte])
        else:
            current_string = dictionary[index] + bytes([byte])
        decompressed_data.extend(current_string)
        dictionary[next_code] = current_string
        next_code += 1

    # Write the decompressed data to a file
    with open(output_file_path, 'wb') as f:
        f.write(decompressed_data)
