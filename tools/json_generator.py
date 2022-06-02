from sizer import calculate_file_size
from hasher import calculate_file_hash
from os import system, path
from json import dumps

class JSONGenerationFailure(Exception):
    ...

class InvalidFilePath(Exception):
    ...

class InvalidPlatformData(Exception):
    ...

class MissingRequiredData(Exception):
    ...

class JSONUtility():
    def __init__(self):
        # App Variables
        self.app_name: str = None
        self.version: str = None
        # (Optional) Update Information
        self.info: str = None
        # Windows Variables
        self.include_win_info: bool = False
        self.path_to_win_release: str = False
        self.win_dl_filename: str = None
        self.win_dl_link: str = None
        self.win_size: str = None
        self.win_md5: str = None
        self.win_sha256: str = None
        # Unix Variables
        self.include_unix_info: bool = False
        self.path_to_unix_release: str = False
        self.unix_dl_filename: str = None
        self.unix_dl_link: str = None
        self.unix_size: str = None
        self.unix_md5: str = None
        self.unix_sha256: str = None

    def get_application_name(self):
        self.app_name = str(input("Application Name: "))
        if self.app_name == "":
            raise MissingRequiredData(f"Please enter a valid application name")

    def get_version(self):
        self.version = str(input("Application Version: "))
        if self.version == "":
            raise MissingRequiredData(f"Please enter a valid version number")

    def check_get_info(self) -> tuple:
        # Ask to Include Release / Update Notes
        # return (T/F for Info Field Data, "" if F or String if T)
        y = ['y', 'yes']
        n = ['n', 'no']
        while True:
            include_info = str(input("Include Brief Release Information? (y/n): "))
            if include_info.lower() in y:
                info = str(input("Enter Release Info to Display: "))
                return (True, info)
            elif include_info.lower() in n:
                return (False, "")
            else:
                print(f"\"{include_info}\" is not a valid response. [Y, Yes, N, No]")

    def get_include_windows(self) -> bool:
        y = ['y', 'yes']
        n = ['n', 'no']
        while True:
            include_windows = str(input("Include Windows Release Information? (y/n): "))
            if include_windows.lower() in y:
                return True
            elif include_windows.lower() in n:
                return False
            else:
                print(f"\"{include_windows}\" is not a valid response. [Y, Yes, N, No]")

    def get_windows_release_filepath(self):
        filepath = str(input("File Path to Windows Release: "))
        if not path.exists(filepath):
            raise InvalidFilePath(f"\"{filepath}\" is not a valid absolute or relative path")
        else:
            self.path_to_win_release = filepath

    def get_windows_release_data(self):
        self.win_size = calculate_file_size(self.path_to_win_release)
        self.win_md5, self.win_sha256 = calculate_file_hash(self.path_to_win_release, buffer_size = 65536)

    def get_windows_dl_name(self):
        self.win_dl_filename = str(input("Name of Windows Release once Downloaded for Clients: "))

    def get_windows_dl_link(self):
        self.win_dl_link = str(input("Enter Windows Release Download Link: "))

    def get_include_unix(self) -> bool:
        y = ['y', 'yes']
        n = ['n', 'no']
        while True:
            include_unix = str(input("Include Unix Release Information? (y/n): "))
            if include_unix.lower() in y:
                return True
            elif include_unix.lower() in n:
                return False
            else:
                print(f"\"{include_unix}\" is not a valid response. [Y, Yes, N, No]")

    def get_unix_release_filepath(self):
        filepath = str(input("File Path to Unix Release: "))
        if not path.exists(filepath):
            raise InvalidFilePath(f"\"{filepath}\" is not a valid absolute or relative path")
        else:
            self.path_to_unix_release = filepath

    def get_unix_release_data(self):
        self.unix_size = calculate_file_size(self.path_to_unix_release)
        self.unix_md5, self.unix_sha256 = calculate_file_hash(self.path_to_unix_release, buffer_size = 65536)

    def get_unix_dl_name(self):
        self.unix_dl_filename = str(input("Name of Unix Release once Downloaded for Clients: "))

    def get_unix_dl_link(self):
        self.unix_dl_link = str(input("Enter Unix Release Download Link: "))

    def get_platform_data(self):
        self.get_application_name()
        self.get_version()
        self.info = self.check_get_info()
        print("")
        self.include_win_info = self.get_include_windows()
        self.include_unix_info = self.get_include_unix()

    def get_and_set_variables(self):
        print("")
        if self.include_win_info:
            self.get_windows_release_filepath()
            self.get_windows_release_data()
            self.get_windows_dl_link()
            self.get_windows_dl_name()
        if self.include_win_info and self.include_unix_info:
            print("")
        if self.include_unix_info:
            self.get_unix_release_filepath()
            self.get_unix_release_data()
            self.get_unix_dl_link()
            self.get_unix_dl_name()
        if not self.include_unix_info and not self.include_win_info:
            raise InvalidPlatformData(f"\"USE_UNIX = {self.include_unix_info}; USE_WIN = {self.include_win_info}\" is invalid platform data - please select one")

    def build_json_file(self):
        host_json = {
            "app_data": {
                "name": self.app_name,
                "version": self.version,
                "update_info": "N/A"
            },
            "win": {
                "name": "N/A",
                "link": "N/A",
                "metadata": {
                    "md5": "N/A",
                    "sha256": "N/A",
                    "size": {
                        "raw_bytes": "N/A",
                        "formatted": "N/A"
                    }
                }
            },
            "unix": {
                "name": "N/A",
                "link": "N/A",
                "metadata": {
                    "md5": "N/A",
                    "sha256": "N/A",
                    "size": {
                        "raw_bytes": "N/A",
                        "formatted": "N/A"
                    }
                }
            }
        }
        if self.info[0]:
            host_json["app_data"]["update_info"] = self.info[1]
        if self.include_win_info:
            host_json["win"]["name"] = self.win_dl_filename
            host_json["win"]["link"] = self.win_dl_link
            host_json["win"]["metadata"]["md5"] = self.win_md5
            host_json["win"]["metadata"]["sha256"] = self.win_sha256
            host_json["win"]["metadata"]["size"]["raw_bytes"] = self.win_size[0]
            host_json["win"]["metadata"]["size"]["formatted"] = self.win_size[1]
        if self.include_unix_info:
            host_json["unix"]["name"] = self.unix_dl_filename
            host_json["unix"]["link"] = self.unix_dl_link
            host_json["unix"]["metadata"]["md5"] = self.unix_md5
            host_json["unix"]["metadata"]["sha256"] = self.unix_sha256
            host_json["unix"]["metadata"]["size"]["raw_bytes"] = self.unix_size[0]
            host_json["unix"]["metadata"]["size"]["formatted"] = self.unix_size[1]
        with open('host.json', 'w') as f:
            f.write(dumps(host_json, indent=4))
        print("\nSuccessfully Created 'host.json' File!\nFeel free to rename it!")

    def run(self):
        self.get_platform_data()
        self.get_and_set_variables()
        self.build_json_file()

if __name__ == '__main__':
    json_gen = JSONUtility()
    json_gen.run()
