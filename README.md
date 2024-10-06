# yt_video_downloader

Экспериментальная загрузка видео

# Python Initialization

Install [[Python]] and [[Package Installer for Python (PIP)|PIP]]:
```sh
sudo apt install python3
sudo apt install python3-pip
#sudo apt install python3.8
python3 --version
```

Install Virtual Environment Package:
```sh
sudo apt install -y python3-venv
```

Now can enter project directory:
```sh
cd path/to/project
```

Create environment:
```sh
python3 -m venv .venv
```
	-m - module-name, finds sys.path and runs corresponding .py file 

Use this environment:
```sh
source .venv/bin/activate
```

---

**Git**

Add this environment to .gitignore:
```sh
echo ".venv" >> .gitignore
```

---

**To recreate environment**

(Already done) Firstly, freeze current environment packages:
```sh
pip freeze > requirements.txt
```

To recreate environment in future, run:
```sh
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```


You can check if it works:
```sh
pip install pytube
```


Updating packages in a virtual environment:
```sh
pip install --upgrade -r requirements.txt
```
