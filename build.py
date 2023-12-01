from PyInstaller.__main__ import run as build

build(["whale.py", "--onefile", "--icon=fav.ico"])
