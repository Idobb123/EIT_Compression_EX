import chardet


def detect_encoding(file_path):
    with open(file_path, 'rb') as file:
        raw_data = file.read(10000)  # Read a portion of the file
        result = chardet.detect(raw_data)
        print(f"Detected encoding: {result['encoding']}")
        print(f"Confidence: {result['confidence']}")

detect_encoding("Samp1.bin")