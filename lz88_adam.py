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

    print(f"Compressed data written to {output_file_path}")


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


if __name__ == "__main__":
    os.makedirs('tests', exist_ok=True)
    MIN_FILE = 1
    MAX_FILE = 5
    RANGE = range(MIN_FILE, MAX_FILE)

    input_files = [f"Samp{i}.bin" for i in RANGE]
    compressed_files = [f"tests/compressed_Samp{i}.bin" for i in RANGE]
    decompressed_files = [f"tests/decompressed_Samp{i}.bin" for i in RANGE]

    for i, (input_file, compressed_file, decompressed_file) in enumerate(
            zip(input_files, compressed_files, decompressed_files)):
        print(f"Processing file {i + 1}...")

        # Compress the file
        print(f"Compressing {input_file}...")
        start_time = time.time()
        lz78_compress(input_file, compressed_file)
        end_time = time.time()

        # Calculate compression ratio
        original_size = os.path.getsize(input_file)
        compressed_size = os.path.getsize(compressed_file)
        compression_ratio = compressed_size / original_size if original_size > 0 else float('inf')

        print(f"\nCompression ratio: {compression_ratio:.2f}")
        print(f"Compression time: {end_time - start_time:.2f} seconds")

        # Decompress the file
        lz78_decompress(compressed_file, decompressed_file)

        # Verify decompressed file matches the original
        with open(input_file, 'rb') as original, open(decompressed_file, 'rb') as decompressed:
            if original.read() == decompressed.read():
                print(f"File {i + 1} successfully verified! The decompressed file matches the original.")
            else:
                print(f"File {i + 1} verification failed! The decompressed file does not match the original.")

