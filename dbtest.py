from flask_pymongo import ObjectId
import uuid
from pymongo import MongoClient
import models

cluster = MongoClient('mongodb+srv://SidAnand:pass@cluster0.69kyd.mongodb.net/test')
db = cluster['test']
collection = db['communities']

# post = {'name': 'sid', 'score': 4}
# collection.insert_one(post)

# models.create_post('sid sid ', 'hi hi ')
# models.create_post('babu babu', 'by by')
#
# collection.insert_one({'class name': 'test', 'subject': 'test', 'posts': []})
# collection.find_one_and_update({'class name': 'test'}, {"$push": {"posts": ['sid', 'test 1']}})
# # print(models.get_post())

# collection.insert_one({'class name': 'test', 'subject': 'subject math', 'posts': {}})
# print(collection.find_one({'class name': 'test'})['posts'][0][0])

# print(collection.find_one({'_id': ObjectId('5f790ce48720ff31123058fe')}))
# content = {{'id': uuid.uuid4().hex, "username": '1', "post": 'test 1', 'replies': {}}}
# collection.find_one_and_update({'_id': ObjectId('5f790ce48720ff31123058fe')},
#                                {"$set": {"posts": content}})


# collection.insert_one({'class name': 'test', 'subject': 'test subject', 'posts': []})
# collection.find_one_and_update({'class name': 'test'}, {"$push": {"posts": ['id 1', 'test user', 'sample', []]}})
# collection.find_one_and_update({'': 'test'}, {"$push": {"posts.Array": [['user 2', 'response']]}})

# collection.find_one_and_update({'class name': 'test'}, {'$push': {'posts.0.3': ['user 3', 'reply']}})
p = 'bye '


for x in range(len(collection.find_one({'class name': 'test'})['posts'])):
    if collection.find_one({'class name': 'test'})['posts'][x][2] == p:
        print(x)



print(collection.find_one({'posts.0.0': 'f52a053be8c54c2e989913ebb5fa1c59' }))
print(collection)
print(collection.find_one({'class name': 'test'}))
