from pymongo import *

cluster = MongoClient('mongodb+srv://SidAnand:pass@cluster0.69kyd.mongodb.net/test')
db = cluster['test']
collection = db['TestPost']


def create_post(name, content):
    collection.insert({'name': name, 'content': content})

def get_post():
    data = list(collection.find({}))
    posts = []
    for item in data:
        posts.append([item['name'], item['content']])
    return posts

