.\env\Scripts\Activate.ps1
pyinstaller --onefile --hidden-import=metric_modules --hidden-import=windows --hidden-import=linux servmon.py
