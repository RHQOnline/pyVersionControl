from os import system, path
from sys import platform, argv
from hashlib import md5, sha256
from requests import get
import json

class AutoUpdater():
    def __init__(self, update_link: str, json_link: str, version: str = "0.0.0", buffer_size: int = 65536, verbose: bool = False) -> None:
        # Identify the Update Link
        self.link_to_download_new_version = update_link
        # Identify the JSON Data File Link
        self.link_to_check_new_version = json_link
        # Identify Current Application's Version
        self.version = version
        # Identify Current Application's Absolute Filepath
        self.current_file = path.abspath(argv[0])
        # Identify Buffer Size for Downloading and Hashing
        self.buffer_size = buffer_size
        # Identify Verbosity Variable for Detailed Output
        self.verbose = verbose
        # Add Definitions for System Platforms
        self.linux_sysplatforms = ["linux", "linux2", "cygwin", "riscos", "atheos", "os2", "os2emx", "freebsd7", "freebsd8", "freebsdN", "freebsd6"]
        self.windows_sysplatforms = ["win32", "msys"]
        self.macOSX_sysplatforms = ["darwin"]
        # Assign the Local System Platform (for Client / User)
        self.platform = platform

    def clear_terminal(self) -> None:
        """
        Basic Function to Clear the Terminal. (Cross-Platform)
        """
        if self.platform in self.linux_sysplatforms or self.platform in self.macOSX_sysplatforms:
            system("clear")
        elif self.platform in self.windows_sysplatforms:
            system("cls")
        else:
            # Unknown OS - Assume UNIX-based
            system("clear")

    def pause_terminal(self) -> None:
        """
        Basic Function to Pause the Terminal. (Cross-Platform)
        """
        if self.platform in self.linux_sysplatforms or self.platform in self.macOSX_sysplatforms:
            if self.verbose:
                input("Press Any Key to Continue...")
            else: input("")
        elif self.platform in self.windows_sysplatforms:
            if self.verbose:
                system("pause")
            else: system("pause>NUL")
        else:
            # Unknown OS - Assume UNIX-based
            if self.verbose:
                input("Press Any Key to Continue...")
            else: system("")

def calculate_file_hash(self, file_abspath: path) -> tuple:
        """
        Basic Function to Hash a File. (Cross-Platform)
         - Takes: Absolute Filepath
         - Gives: Tuple(MD5_Hash, SHA256_Hash)
        """
        md5hasher = md5()
        sha256hasher = sha256()
        with open(file_abspath, 'rb') as f:
            while True:
                data = f.read(self.buffer_size)
                if not data:
                    break
                md5hasher.update(data)
                sha256hasher.update(data)
            md5hash = md5hasher.hexdigest()
            sha256hash = sha256hasher.hexdigest()
        return (md5hash, sha256hash)

    def calculate_file_size(self, file_abspath: path) -> str:
        size = path.getsize(file_abspath)
        magnitude = 0
        while abs(size) >= 1024:
            magnitude += 1
            size /= 1024.0
        return "%.2f %s" % (size, ['bytes', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB'][magnitude])

    def compare_file_hashes(self, hash_one: str, hash_two: str) -> bool:
        """
        Basic Function to Compare Two File Hashes. (Cross-Platform)
         - Takes: 2x File Hashes (any kind, preferrably MD5/SHA256)
         - Gives: Boolean of True / False for Matching Hashes
        """
        return True if hash_one == hash_two else False

    def compare_file_sizes(self, size_one: str, size_two: str) -> bool:
        """
        Basic Function to Compare Two File Sizes. (Cross-Platform)
         - Takes: 2x File Sizes
         - Gives: Boolean of True / False for Matching Sizes
        """
        return True if size_one == size_two else False
