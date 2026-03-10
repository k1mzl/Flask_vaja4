#tinyDB in request IP
from tinydb import tinydb

db = TinyDB('obiskovalci.json')


db.insert({'IP':'192.168.1.1'})


# /obiskovalci route
print(db.all())