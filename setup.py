import sys
import os
import platform
from cx_Freeze import setup, Executable

base = None
if sys.platform == 'win32':
    base = 'Win32GUI'

if platform.system() == "Windows":
    PYTHON_DIR = os.path.dirname(os.path.abspath(__file__))
    os.environ['TCL_LIBRARY'] = "C:\\Users\\Karthikeyan\\AppData\\Local\\Programs\\Python\\Python36-32\\tcl\\tcl8.6"
    os.environ['TK_LIBRARY'] = "C:\\Users\\Karthikeyan\\AppData\\Local\\Programs\\Python\\Python36-32\\tcl\\tk8.6"


executables = [
    Executable('testing_app.py', targetName='sample.exe', base=base)
]

options = {
    'build_exe': {
        # Sometimes a little fine-tuning is needed
        # exclude all backends except wx
        'include_files': ['chromedriver.exe', (os.path.join(PYTHON_DIR, 'DLLs', 'tcl86t.dll'), ''),
                          (os.path.join(PYTHON_DIR, 'DLLs', 'tk86t.dll'), ''),
                          (os.path.join(PYTHON_DIR, 'DLLs', 'sqlite3.dll'), '')]
    }
}

setup(name='simple_Tkinter',
      version='0.1',
      description='Sample cx_Freeze Tkinter script',
      executables=executables,
      options=options

      )
