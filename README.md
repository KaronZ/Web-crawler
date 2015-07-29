# Web-crawler
===================
to run this project , the following module is required:

1. python-dev
2. build-essential
3. python-pip

then use `pip install -r requirements.txt` to install python library

Introduction
==================
Use Python to achieve the goal to get the data from the v2ex webstie. The data is stored in mysqldb.

Notice
==================
mysql use 3 bytes to present a unicode char, while 4 bytes are needed. 

Do remember to use `CREATE DATABASE vendoremail CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci` when creating databases.
