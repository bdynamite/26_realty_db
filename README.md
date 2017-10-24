# Real Estate Site

This app shows flats from database with some filtres

# How to Install

Python 3 should be already installed. Then use pip (or pip3 if there is a conflict with old Python 2 setup) to install dependencies:

```bash
pip install -r requirements.txt # alternatively try pip3
```

# Quickstart


Example of script launch on Windows, Python 3.5:

How to create database

```#!bash

$ python db_manager.py

```
then you will find realty.db in the script folder

How to update database

```#!bash

$ python db_manager.py -f [path to json file]

```
realty.db will be filled by your json file

How to run

```#!bash

$ python server.py

```

then open [http://127.0.0.1:5000/](http://127.0.0.1:5000/)
# Project Goals

The code is written for educational purposes. Training course for web-developers - [DEVMAN.org](https://devman.org)
