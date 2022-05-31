# pyVersionControl - FOSS VCS and Launcher / Updater!
pyVersionControl is a free, open-source, cross-platform, Python-based TUI/GUI Application/Client Launcher and Updater, with an included library to drop into your existing applications for ease of implementation!

<div align="center">
<b>Repository Statistics and Information</b>
<br>
<img alt="License" src="https://img.shields.io/github/license/RHQOnline/pyVersionControl">
<img alt="GitHub Repo Size" src="https://img.shields.io/github/repo-size/RHQOnline/pyVersionControl">
<img alt="GitHub Code Size in Bytes" src="https://img.shields.io/github/languages/code-size/RHQOnline/pyVersionControl">
<img alt="Lines of Code" src="https://img.shields.io/tokei/lines/github/RHQOnline/pyVersionControl">
<br>
<img alt="GitHub Release (Latest SemVer)" src="https://img.shields.io/github/v/release/RHQOnline/pyVersionControl?color=maroon&label=latest%20release">
<img alt="GitHub Downloads - All Releases" src="https://img.shields.io/github/downloads/RHQOnline/pyVersionControl/total">
<br><br>
<b>Repository Activity Statistics</b>
<br>
<img alt="GitHub Issues" src="https://img.shields.io/github/issues-raw/RHQOnline/pyVersionControl">
<img alt="GitHub Pull Requests" src="https://img.shields.io/github/issues-pr-raw/RHQOnline/pyVersionControl">
<br>
<img alt="GitHub Closed Issues" src="https://img.shields.io/github/issues-closed-raw/RHQOnline/pyVersionControl">
<img alt="GitHub Closed Pull Requests" src="https://img.shields.io/github/issues-pr-closed-raw/RHQOnline/pyVersionControl">
</div>

## Raison D'être
The Python Developer User-Space is currently lacking of a consistent, stable, and performant auto-updater or software launcher. This is a rather large hole in the community that, in our opinion, needs to be addressed. This repository and it's contents serve as a one-size-fits-all solution to this issue, allowing users to have access to a cross-platform, performant auto-updating library to be built into their own applications, or to build a launcher and updater around an existing application.

## Installation
`git clone https://github.com/RHQOnline/pyVersionControl` or head to the [Releases Page](https://github.com/RHQOnline/pyVersionControl/releases/latest)

## Usage
This section details usage for the library, the (upcoming) GUI Launcher, and the Tools.

### `auto_updater.py`
- Drag'n'Drop `auto_updater.py` into your `/src` directory or your project directory
- Import it via `from auto_updater import AutoUpdater`
- Create the `AutoUpdater` Object by Initializing it: `updater = AutoUpdater(application_name = "ApplicationName", json_link = "https://raw.githubusercontent.com/YourUsername/YourRepo/main/your.json", version = "1.0.0", newfile = False, buffer_size = 65536, verbose = False)`
- Call the Update Task with `updater.attempt_update()`
- Enjoy! :)

#### Parameters for the `AutoUpdater()` Object
|    Parameter     |    Default Value    |       Description        |
| ---------------- | ------------------- | ------------------------ |
| application_name | Example Application | Name of Your Application |
| json_link        | 127.0.0.1/host.json | The Link to Your Remote .json Host / Status File |
| version          | 1.0.0 | The Version of Your Application |
| newfile          | True | If `True`, Creates New File for Updated Application; If `False`, Overwrites Existing Application |
| buffer_size | 65536 | Size of the Buffer (in Bytes) for Reading / Writing Files |
| verbose | False | Verbosity Toggle (Detailed Output in Terminal of Update Task) |

### `hasher.py` and `sizer.py`
- CD / ChDir into `/tools`
- Run `hasher.py` or `sizer.py` with the desired file as the only argument
  - Example (Script Usage): `python hasher.py ../dist/my_app.exe`
  - Example (Binary Usage): `./sizer dist/my_app` (Linux) or `sizer(.exe) dist/my_app.exe`

#### Arguments for `hasher.py` and `sizer.py`
| Argument | Default Value | Description |
| -------- | ------------- | ----------- |
| filename | N/A | Absolute or Relative File Path to Desired File |

## Features
 - TUI/GUI Launcher Builds (customisable)
   - Ready-to-Go, Configurable Launchers
   - Basic, but Highly Extensible
 - Auto-Updating Ability / Package
   - Exists Standalone from Launchers
   - Plug'n'Play with Pre-Existing Applications
     - Drop `auto_updater.py` into your sources for your program
     - `from auto_updater import AutoUpdater`
     - `updater = AutoUpdater()` to Create the Object (use parameters)
     - `updater.generate_template_json()` to Create the Templated (Mostly-Correct) Host `.json` File
       - Use the [Tools](https://github.com/RHQOnline/pyVersionControl/tree/main/tools) to Fix / Adjust Values
     - `updater.attempt_update()` to Spawn Task for Update Check
   - Users don't have to manually download your new builds any more
 - Hashing and File Sizing Utilities
   - This is so users can properly update their host `.json` file
   - See the [Tools](https://github.com/RHQOnline/pyVersionControl/tree/main/tools) Directory
     - Contains `hasher.py` and `sizer.py`
 - Full Cross-Platform Support
   - Linux
   - Windows (x32, x64)
   - MacOS

## Roadmap
 - Implement Error and Exception Handling
 - Build GUI Version for Launcher (Template)
