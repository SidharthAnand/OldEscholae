from pymongo import MongoClient
import models

cluster = MongoClient('mongodb+srv://SidAnand:pass@cluster0.69kyd.mongodb.net/test')
db = cluster['test']
collection = db['TestPost']

# post = {'name': 'sid', 'score': 4}
# collection.insert_one(post)

# models.create_post('sid sid ', 'hi hi ')
# models.create_post('babu babu', 'by by')
print(models.get_post())