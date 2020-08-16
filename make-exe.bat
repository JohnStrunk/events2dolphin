del events2dolphin.exe

python -m venv venv
call venv\Scripts\activate.bat

python -m pip install --upgrade pip
pip install --upgrade -r requirements.txt

pyinstaller --onefile --distpath=. --workpath=build --version-file=events2dolphin.version events2dolphin.py

del events2dolphin.spec
rmdir /q/s build