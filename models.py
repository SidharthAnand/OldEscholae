from pymongo import *
from flask import *

cluster = MongoClient('mongodb+srv://SidAnand:pass@cluster0.69kyd.mongodb.net/test')
db = cluster['test']


def create_post(name, content):
    collection = db['TestPost']
    collection.insert({'name': name, 'content': content})
    print('post created')


def get_post():
    collection = db['TestPost']
    data = list(collection.find({}))
    posts = []
    for item in data:
        posts.append([item['name'], item['content']])
    print('post read')
    return posts


def get_docs(collection):
    return reversed(list(collection.find({})))


def login_redirect():
    if 'username' not in session:
        flash('Session Expired. Please Login Again')
        redirect('/login')


def logout():
    if 'username' in session:
        del session['username']
    return redirect('/login')

