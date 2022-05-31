from os import system, path, replace
from sys import platform, argv
from hashlib import md5, sha256
from requests import get
import json

class AutoUpdater():
    def __init__(self, application_name: str = "Example Application", json_link: str = "127.0.0.1/host.json", version: str = "0.0.0", binaryfile: bool = True, newfile: bool = True, buffer_size: int = 65536, verbose: bool = False) -> None:
        # Application Name
        self.app_name = application_name
        # Mode: Newfile (True; creates new file for download) or Overwrite (False; overwrites existing file / current application)
        self.newfile = newfile
        # Mode: Binaryfile (True; makes downloaded files executable for Unix systems) or Nonbinaryfile (False; does nothing to downloaded file)
        self.binaryfile = binaryfile
        # Identify the JSON Data File Link
        self.json_link = json_link
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
        # Assign the Status Data
        self.status_data = self.get_status_json_data()
        # Assign the Detail Variables for Current File / Application
        self.md5_hash, self.sha256_hash = self.calculate_file_hash(self.current_file)
        self.cur_file_size = self.calculate_file_size(self.current_file)

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

    def calculate_file_hash(self, file_abspath: str) -> tuple:
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

    def calculate_file_size(self, file_abspath: str) -> str:
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

    def generate_template_json(self) -> None:
        """
        Basic Function to Generate a Template Hosting JSON File. (Cross-Platform)
        """
        template_dict = {
            "Application Name": self.app_name,
            "Version": self.version,
            "File Name (Windows)": argv[0],
            "Link to Download (Windows)": "Link goes here to your release's .zip or .exe, etc.",
            "File Name (Unix)": argv[0],
            "Link to Download (Unix)": "Link goes here to your release's .zip or .exe, etc.",
            "Update Information": "Example Hotfix Information (Short&Sweet)",
            "MD5 Hash": f"CHANGEME: {self.md5_hash}",
            "SHA256 Hash": f"CHANGEME: {self.sha256_hash}",
            "File Size": f"CHANGEME: {self.cur_file_size}"
        }
        with open('example_host_json.json', 'w') as f:
            f.write(json.dumps(template_dict, indent = 4))

    def get_status_json_data(self) -> dict:
        """
        Basic Function to Check a Hosting JSON File. (Cross-Platform)
        """
        return json.loads(get(self.json_link).content)

    def check_for_update(self) -> tuple:
        """
        Basic Function to Check a Hosting JSON File. (Cross-Platform)
         - Checks: File Sizes and MD5/SHA256 Hashes
         - Does:   Returns True if an Update is Needed, False if Not, and the DL Link Regardless
        """
        sizes_match = False
        hashes_match = False
        versions_match = False
        if self.status_data["File Size"] == self.cur_file_size:
            sizes_match = True
            if self.verbose:
                print(f"{'Sizes Match!'}")
        if self.status_data["MD5 Hash"] == self.md5_hash and self.status_data["SHA256 Hash"] == self.sha256_hash:
            hashes_match = True
            if self.verbose:
                print(f"{'Hashes Match!'}")
        if self.status_data["Version"] == self.version:
            versions_match = True
            if self.verbose:
                print(f"{'Versions Match!'}")
        return (False if versions_match and hashes_match and sizes_match else True, self.status_data["Link to Download (Windows)"], self.status_data["Link to Download (Unix)"])

    def attempt_update(self) -> bool:
        """
        The Main Logic of the Auto-Updater. This will...
         - Check if an Update is Needed
         - If it is, Download it
         - If it isn't, Skip it and Proceed
         - Exception Handling for Offline / No Internet Access
         - Overwrite Current File or DL as New File
        """
        # Check for Updates and Fetch Link
        update_needed, dl_link_windows, dl_link_unix = self.check_for_update()
        if self.verbose:
            print(f"Checked for Updates: Found '{'NEEDS UPDATE' if update_needed else 'NO UPDATE NEEDED'}'!")
        # If an update is needed
        if update_needed:
            # If the developer specified newfile mode
            if self.newfile:
                if self.platform in self.windows_sysplatforms:
                    with open(f'{self.status_data["File Name (Windows)"]}', 'wb') as f:
                        f.write(get(dl_link_windows).content)
                elif self.platform in self.linux_sysplatforms or self.platform in self.macOSX_sysplatforms:
                    with open(f'{self.status_data["File Name (Unix)"]}', 'wb') as f:
                        f.write(get(dl_link_unix).content)
                    if self.binaryfile:
                        system(f'chmod +x "{self.status_data["File Name (Unix)"]}"')
                else:
                    # Unknown OS - Assume UNIX-based
                    with open(f'{self.status_data["File Name (Unix)"]}', 'wb') as f:
                        f.write(get(dl_link_unix).content)
                    if self.binaryfile:
                        system(f'chmod +x "{self.status_data["File Name (Unix)"]}"')
                return True
            # If the developer specified overwrite mode
            else:
                # Hacky Workaround to System File Locks ;)
                current_file_name = argv[0]
                current_file_mod = f"{current_file_name}.tmp"
                if self.platform in self.windows_sysplatforms:
                    with open(current_file_mod, 'wb') as f:
                        f.write(get(dl_link_windows).content)
                elif self.platform in self.linux_sysplatforms or self.platform in self.macOSX_sysplatforms:
                    with open(current_file_mod, 'wb') as f:
                        f.write(get(dl_link_unix).content)
                else:
                    # Unknown OS - Assume UNIX-based
                    with open(current_file_mod, 'wb') as f:
                        f.write(get(dl_link_unix).content)
                replace(current_file_mod, current_file_name)
                if self.platform in self.linux_sysplatforms or self.platform in self.macOSX_sysplatforms:
                    if self.binaryfile:
                        system(f"chmod +x \"{current_file_name}\"")
                return True
        # If an update is not needed
        else:
            if self.verbose:
                print("No update needed; skipping update / patch task!")
            return False
