from os import path
from sys import argv

class SizeFailure(Exception):
    ...

def calculate_file_size(file_abspath: str) -> tuple:
    """
    Basic Function to Size a File. (Cross-Platform)
    - Takes: Absolute Filepath
    - Gives: String of File Size
    """
    size = path.getsize(file_abspath)
    og_size = size
    magnitude = 0
    while abs(size) >= 1024:
        magnitude += 1
        size /= 1024.0
    return (og_size, "%.2f %s" % (size, ['bytes', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB'][magnitude]))

if __name__ == '__main__':
    if argv[1]:
        try:
            raw, readable = calculate_file_size(argv[1])
            print(f"File Size (Raw): {raw}\nFile Size (Readable): {readable}")
        except:
            raise SizeFailure("Failed to Size File! Please provide an absolute or relative filepath!")
    else:
        raise SizeFailure("Failed to Size File! Please provide an absolute or relative filepath!")
