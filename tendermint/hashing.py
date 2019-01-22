import os
import hashlib


# lets read stuff in 64kb chunks! Since model file can be HUGE
BUF_SIZE = 65536  

# Hashing library to be used
# right now using sha256
hash_function = hashlib.sha256()

# Function to make sure the file path is same
def get_file_path(rel_path):
    script_dir = os.path.dirname(__file__)
    abs_file_path = os.path.join(script_dir, rel_path)
    return abs_file_path

# Function to return hash of a large file
def get_hash_of_file(rel_path):
    file_path = get_file_path(rel_path)

    # Read the file in small chunks and calculate the hash
    with open(file_path, 'rb') as f:
        while True:
            data = f.read(BUF_SIZE)
            if not data:
                break
            hash_function.update(data)

    return format(hash_function.hexdigest())