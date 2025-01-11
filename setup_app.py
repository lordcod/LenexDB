import os
from pathlib import Path
parent = Path(__file__).parent
packages = parent / '.venv' / 'Lib' / 'site-packages'
filename = parent / 'menu.py'

command = f"pyinstaller --onedir --paths {packages} --noconfirm --noconsole {filename}"
os.system(command)