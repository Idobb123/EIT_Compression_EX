import os

from lz88_adam import lz78_compress, lz78_decompress
from huffman import huffman_compress, huffman_decompress

if __name__ == "__main__":
    num_of_loops = 0
    os.makedirs("tests", exist_ok=True)
    MIN_FILE = 1
    MAX_FILE = 5
    RANGE = range(MIN_FILE, MAX_FILE)

    input_files = [f"Samp{i}.bin" for i in RANGE]
    mid_files = [f"midSamp{i}.bin" for i in RANGE]
    compressed_files = [f"tests/compressed_Samp{i}.bin" for i in RANGE]
    decompressed_files = [f"tests/decompressed_Samp{i}.bin" for i in RANGE]

    for i, (input_file, mid_file, compressed_file, decompressed_file) in enumerate(
            zip(input_files, mid_files, compressed_files, decompressed_files)):
        print(f"Processing file {i + 1}...")

        # Compress the file
        print(f"Compressing {input_file}...")

        huffman_compress(input_file, compressed_file)

        # Calculate compression ratio
        original_size = os.path.getsize(input_file)
        compressed_size = os.path.getsize(compressed_file)
        compression_ratio = compressed_size / original_size if original_size > 0 else float('inf')

        print(f"\nCompression ratio: {compression_ratio:.3f}")

        huffman_decompress(compressed_file, decompressed_file)

        # Verify decompressed file matches the original
        with open(input_file, 'rb') as original, open(decompressed_file, 'rb') as decompressed:
            if original.read() == decompressed.read():
                print(f"File {i + 1} successfully verified! The decompressed file matches the original.")
            else:
                print(f"File {i + 1} verification failed! The decompressed file does not match the original.")
