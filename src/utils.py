from os import system
from sys import platform

linux_sysplatforms = ["linux", "linux2", "cygwin", "riscos", "atheos", "os2", "os2emx", "freebsd7", "freebsd8", "freebsdN", "freebsd6"]
windows_sysplatforms = ["win32", "msys"]
macOSX_sysplatforms = ["darwin"]

def clear_terminal():
  if platform in linux_sysplatforms or platform in macOSX_sysplatforms:
    system("clear")
  elif platform in windows_sysplatforms:
    system("cls")
  else:
    # Unknown OS - Assume UNIX-based
    system("clear")
