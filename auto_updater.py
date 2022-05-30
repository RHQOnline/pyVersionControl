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
