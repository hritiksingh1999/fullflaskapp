from pymongo import MongoClient
from bson.json_util import dumps
client = MongoClient('mongodb://localhost:27017')
db = client.emptyl


username=db.username
posts=db.post
comment=db.comment
 