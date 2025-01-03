import os
import time
from dahuffman import HuffmanCodec
from bitarray import bitarray
import pickle

class LZ78Compressor:
    """
    A simplified implementation of the LZ78 Compression Algorithm
    """

    def __init__(self):
        self.dictionary = {}
        self.reverse_dictionary = {}

    def compress(self, input_file_path, output_file_path=None, verbose=False):
        """
        Compresses the file using LZ78.
        """
        # Read the input file
        try:
            with open(input_file_path, 'rb') as input_file:
                data = input_file.read()
        except IOError:
            print("Could not open input file.")
            raise

        self.dictionary = {}
        compressed_data = []
        current_string = b""
        dictionary_index = 1

        for byte in data:
            current_string += bytes([byte])
            if current_string not in self.dictionary:
                self.dictionary[current_string] = dictionary_index
                if len(current_string) > 1:
                    prefix = current_string[:-1]
                    compressed_data.append((self.dictionary[prefix], byte))
                else:
                    compressed_data.append((0, byte))
                dictionary_index += 1
                current_string = b""

        if current_string:
            print("curr string :", current_string)
            prefix = current_string[:-1]
            compressed_data.append((self.dictionary[prefix], current_string[-1]))

        # Serialize compressed data
        encoded_data = bitarray(endian='big')
        for index, next_char in compressed_data:
            encoded_data.frombytes(index.to_bytes(2, 'big'))
            encoded_data.frombytes(bytes([next_char]))

        # Huffman encode the bitstream
        codec = HuffmanCodec.from_data(encoded_data.tobytes())
        huffman_encoded = codec.encode(encoded_data.tobytes())

        # Write to output file
        if output_file_path:
            try:
                with open(output_file_path, 'wb') as output_file:
                    pickle.dump((huffman_encoded, codec), output_file)
                    print("File compressed successfully.")
            except IOError:
                print("Could not write to output file.")
                raise
        else:
            return huffman_encoded

    def decompress(self, input_file_path, output_file_path=None):
        """
        Decompresses a file compressed with LZ78.
        """
        try:
            with open(input_file_path, 'rb') as input_file:
                huffman_encoded, codec = pickle.load(input_file)
        except IOError:
            print("Could not open input file.")
            raise

        # Decode Huffman encoded data
        decoded_data = codec.decode(huffman_encoded)
        encoded_data = bitarray(endian='big')
        encoded_data.frombytes(decoded_data)

        # Deserialize compressed data
        compressed_data = []
        while len(encoded_data) >= 24:
            index = int.from_bytes(encoded_data[:16].tobytes(), 'big')
            next_char = encoded_data[16:24].tobytes()[0]
            compressed_data.append((index, next_char))
            del encoded_data[:24]

        # Rebuild the original data
        self.reverse_dictionary = {0: b""}
        decompressed_data = []
        dictionary_index = 1

        for index, next_char in compressed_data:
            prefix = self.reverse_dictionary[index]
            current_string = prefix + bytes([next_char])
            decompressed_data.append(current_string)
            self.reverse_dictionary[dictionary_index] = current_string
            dictionary_index += 1

        decompressed_data = b"".join(decompressed_data)

        # Write to output file
        if output_file_path:
            try:
                with open(output_file_path, 'wb') as output_file:
                    output_file.write(decompressed_data)
                    print("File decompressed successfully.")
            except IOError:
                print("Could not write to output file.")
                raise
        else:
            return decompressed_data

if __name__ == "__main__":
    MIN_FILE = 1
    MAX_FILE = 5
    RANGE = range(MIN_FILE, MAX_FILE)

    input_files = [f"Samp{i}.bin" for i in RANGE]
    compressed_files = [f"compressed_Samp{i}.bin" for i in RANGE]
    decompressed_files = [f"decompressed_Samp{i}.bin" for i in RANGE]

    lz78 = LZ78Compressor()

    for i, (input_file, compressed_file, decompressed_file) in enumerate(zip(input_files, compressed_files, decompressed_files)):
        print(f"Processing file {i + 1}...")

        # try:
        # Compress the file
        print(f"Compressing {input_file}...")
        start_time = time.time()
        lz78.compress(input_file, compressed_file)
        end_time = time.time()

        # Calculate compression ratio
        original_size = os.path.getsize(input_file)
        compressed_size = os.path.getsize(compressed_file)
        compression_ratio = compressed_size / original_size if original_size > 0 else float('inf')

        print(f"\nOriginal size: {original_size} bytes")
        print(f"Compressed size: {compressed_size} bytes")
        print(f"Compression ratio: {compression_ratio:.2f}")
        print(f"Compression time: {end_time - start_time:.2f} seconds")

        # Decompress the file
        print(f"Decompressing {compressed_file}...")
        lz78.decompress(compressed_file, decompressed_file)

        # Verify decompressed file matches the original
        with open(input_file, 'rb') as original, open(decompressed_file, 'rb') as decompressed:
            if original.read() == decompressed.read():
                print(f"File {i + 1} successfully verified! The decompressed file matches the original.")
            else:
                print(f"File {i + 1} verification failed! The decompressed file does not match the original.")

        # except Exception as e:
        #     print(f"An error occurred with file {i + 1}: {e}")
