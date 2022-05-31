from os import path
from sys import argv

class SizeFailure(Exception):
    ...

def calculate_file_size(file_abspath: str) -> tuple:
    size = path.getsize(file_abspath)
    magnitude = 0
    while abs(size) >= 1024:
        magnitude += 1
        size /= 1024.0
    return ("%.2f %s" % (size, ['bytes', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB'][magnitude]), size)

if __name__ == '__main__':
    if argv[1]:
        try:
            readable, raw = calculate_file_size(argv[1])
            print(f"File Size (Raw): {raw}\nFile Size (Readable): {readable}")
        except:
            raise SizeFailure("Failed to Size File! Please provide an absolute or relative filepath!")
    else:
        raise SizeFailure("Failed to Size File! Please provide an absolute or relative filepath!")
