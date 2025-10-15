# build.sh
source env/bin/activate
pyinstaller --onefile --hidden-import=metric_modules --hidden-import=windows --hidden-import=linux servmon.py
