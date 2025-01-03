import time
import zstandard as zstd
import brotli
import lzma
import bz2
import gzip
import os
import subprocess

def compress_files(file_paths):
    results = {}

    # Define compression algorithms
    compression_algorithms = {
        "zstd": lambda d: zstd.ZstdCompressor(level=22).compress(d),
        "brotli": lambda d: brotli.compress(d, quality=11),
        "lzma": lambda d: lzma.compress(d, preset=9),
        "bzip2": lambda d: bz2.compress(d, compresslevel=9),
        "gzip": lambda d: gzip.compress(d, compresslevel=9),
        "paq": lambda path: compress_with_paq(path),
        "zpaq": lambda path: compress_with_zpaq(path),
    }

    # Initialize results
    for algo in compression_algorithms:
        results[algo] = {
            "total_time": 0,
            "total_ratio": 0,
            "file_ratios": [],
            "count": 0,
        }

    # Process each file
    for file_path in file_paths:
        with open(file_path, "rb") as f:
            data = f.read()
        original_size = len(data)

        print(f"\nProcessing {file_path} (Original size: {original_size} bytes):")

        for algo, compress in compression_algorithms.items():
            try:
                start_time = time.time()
                if algo in ["paq", "zpaq"]:
                    compressed_size = compress(file_path)
                else:
                    compressed_data = compress(data)
                    compressed_size = len(compressed_data)
                end_time = time.time()

                compression_ratio = compressed_size / original_size

                # Update results
                results[algo]["total_time"] += end_time - start_time
                results[algo]["total_ratio"] += compression_ratio
                results[algo]["file_ratios"].append(compression_ratio)
                results[algo]["count"] += 1

                # Print per-file results
                print(f"  {algo}:")
                print(f"    Compressed Size: {compressed_size} bytes")
                print(f"    Compression Ratio: {compression_ratio:.4f}")
                print(f"    Time Taken: {end_time - start_time:.4f} seconds")

            except Exception as e:
                print(f"  {algo}: Failed with error: {e}")

    # Calculate and print averages
    print("\nAverage Results Across All Files:")
    print("-" * 40)
    for algo, result in results.items():
        if result["count"] > 0:
            avg_time = result["total_time"] / result["count"]
            avg_ratio = result["total_ratio"] / result["count"]
            print(f"Algorithm: {algo}")
            print(f"  Average Time Taken: {avg_time:.4f} seconds")
            print(f"  Average Compression Ratio: {avg_ratio:.4f}")
            print(f"  Ratios Per File: {', '.join(f'{r:.4f}' for r in result['file_ratios'])}")
            print("-" * 40)
        else:
            print(f"Algorithm {algo}: No successful compression.")

def compress_with_paq(file_path):
    # Compress using paq8pxd command-line tool
    compressed_file = f"{file_path}.paq8pxd"
    try:
        subprocess.run(["paq8pxd", "output", file_path], check=True)
        compressed_size = os.path.getsize("output.paq8pxd")
        os.rename("output.paq8pxd", compressed_file)  # Rename output
        return compressed_size
    finally:
        # Cleanup
        if os.path.exists("output.paq8pxd"):
            os.remove("output.paq8pxd")

def compress_with_zpaq(file_path):
    # Compress using zpaq command-line tool
    compressed_file = f"{file_path}.zpaq"
    try:
        subprocess.run(["zpaq", "a", compressed_file, file_path], check=True)
        compressed_size = os.path.getsize(compressed_file)
        return compressed_size
    finally:
        # Cleanup
        if os.path.exists(compressed_file):
            os.remove(compressed_file)

# List of file paths
file_paths = [f"Samp{i}.bin" for i in range(1, 5)]

# Run the compression
compress_files(file_paths)
