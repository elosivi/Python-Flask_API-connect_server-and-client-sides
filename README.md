# Python-Flask_API-connect_server-and-client-sides
 2 app developped with Python &amp; Flask. First one : app.py is the server side, the second, client.py the client side. Client can access to data of server (users and articles data), can login, register and delete too.
database is with sqlite3

*****************************************

1/Install Flask
python3 -m pip install flask
dnf install python3-pip (on fedora) : create the script /usr/bin/pip3


2/instal sqlite3
>>>sudo dnf install sqlite3
>>>sqlite3 + help to command


3/ To use the 2 app in localhost:
Open each app in a EDI/terminal:

-----------------
app.py:

>>>export FLASK_APP:app.py export FLASK_DEBUG:true
>>>flask run

this app will run on port:5000 
you can test it with postman.

login + POST
register + POST
users + GET/PUT
users/id + GET/DELETE/POST
artciles + GET/PUT
artciles/id + GET/DELETE/POST

------------------
client.py:

>>>export FLASK_APP:client.py export FLASK_DEBUG:true
>>>flask run --port:3000
this app will run on port:3000
you can use it with your browser.

------------------
