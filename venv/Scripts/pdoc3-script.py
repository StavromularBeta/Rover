#!"T:\ANALYST WORK FILES\Peter\Rover\venv\Scripts\python.exe"
# EASY-INSTALL-ENTRY-SCRIPT: 'pdoc3==0.7.4','console_scripts','pdoc3'
__requires__ = 'pdoc3==0.7.4'
import re
import sys
from pkg_resources import load_entry_point

if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
    sys.exit(
        load_entry_point('pdoc3==0.7.4', 'console_scripts', 'pdoc3')()
    )
