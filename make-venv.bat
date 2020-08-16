python -m venv venv

call venv\Scripts\activate.bat

::: Upgrade pip to latest
python -m pip install --upgrade pip

pip install --upgrade -r requirements.txt
