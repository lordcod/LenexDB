import os
from pathlib import Path
parent = Path(__file__).parent
packages = parent / '.venv' / 'Lib' / 'site-packages'
filename = parent / 'app' / 'menu.py'

command = f"pyinstaller --add-data \"data.json;.\" --add-data \"FINA_Points_Table_Base_Times.xlsx;.\" --onedir --paths {packages} --noconfirm  --noconsole {filename}"
print(command)
os.system(command)