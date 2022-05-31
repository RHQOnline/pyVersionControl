from hashlib import md5, sha256
from sys import argv

class HashFailure(Exception):
    ...

def calculate_file_hash(file_abspath: str, buffer_size: int) -> tuple:
    """
    Basic Function to Hash a File. (Cross-Platform)
        - Takes: Absolute Filepath
        - Gives: Tuple(MD5_Hash, SHA256_Hash)
    """
    md5hasher = md5()
    sha256hasher = sha256()
    with open(file_abspath, 'rb') as f:
        while True:
            data = f.read(buffer_size)
            if not data:
                break
            md5hasher.update(data)
            sha256hasher.update(data)
        md5hash = md5hasher.hexdigest()
        sha256hash = sha256hasher.hexdigest()
    return (md5hash, sha256hash)

if __name__ == '__main__':
    if argv[1]:
        try:
            md5hash, sha256hash = calculate_file_hash(argv[1], 65536)
            print(f"MD5 File Hash: {md5hash}\nSHA256 File Hash: {sha256hash}")
        except:
            raise HashFailure("Failed to Hash File! Please provide an absolute or relative filepath!")
    else:
        raise HashFailure("Failed to Hash File! Please provide an absolute or relative filepath!")
