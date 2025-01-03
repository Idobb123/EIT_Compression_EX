import os

from lz88_adam import lz78_compress, lz78_decompress
from huffman import huffman_compress, huffman_decompress

if __name__ == "__main__":
    # TODO figure out how to run ot in loop successfully
    # TODO make code more readable + typing and docs
    # TODO is LZ should not be used?

    os.makedirs("tests", exist_ok=True)
    MIN_FILE = 1
    MAX_FILE = 5
    for i in range(MIN_FILE, MAX_FILE):
        input_file = f"Samp{i}.bin"  # The file you want to compress
        compressed_file = f"tests/compressed{i}.bin"
        decompressed_file = f"tests/decompressed{i}.bin"

        # Compression step
        huffman_compress(input_file, compressed_file)

        # Decompression step
        huffman_decompress(compressed_file, decompressed_file)

        # print stats
        original_size = os.path.getsize(input_file)
        compressed_size = os.path.getsize(compressed_file)
        compression_ratio = compressed_size / original_size if original_size > 0 else float('inf')

        print(f"\nCompression ratio: {compression_ratio:.3f}")

        with open(input_file, 'rb') as original, open(decompressed_file, 'rb') as decompressed:
            if original.read() == decompressed.read():
                print(f"successfully verified! The decompressed file number {i} matches the original.")
            else:
                print(f"verification failed! The decompressed file number {i} does not match the original.")