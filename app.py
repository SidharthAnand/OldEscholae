from models import *
from flask_pymongo import PyMongo
from flask_pymongo import ObjectId
import uuid

#add the security lines here
app = Flask(__name__)
# Boostrap{app}

app.config['MONGO_URI'] = 'mongodb+srv://SidAnand:pass@cluster0.69kyd.mongodb.net/test'
app.config['SECRET_KEY'] = "SomeSecretText"

mongo = PyMongo(app)


@app.route('/forum', methods=['GET', 'POST'])
def view():
    if 'username' not in session:
        flash('Session Expired. Please Login Again')
        return redirect('/')

    if request.method == 'GET':
        pass

    posts = reversed(get_post())
    return render_template('main.html', posts=posts)


@app.route('/add-post', methods=['GET', 'POST'])
def add_post():
    if 'username' not in session:
        flash('Session Expired. Please Login Again')
        return redirect('/')

    if request.method == 'GET':
        pass

    if request.method == 'POST':
        name = session['username']
        post = request.form['post']
        create_post(name, post)
        return redirect('/forum')

    return render_template('add_posts.html')


@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        if 'username' in session:
            return redirect('/forum')
        return render_template('login.html')

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        collection = mongo.db.users

    user = collection.find_one({'username': username})

    if user and password == user['password']:
        session['username'] = username
        return redirect('/forum')
    else:
        flash('The username and password incorrect')
        return redirect('/')


@app.route('/logout')
def logout():
    if 'username' in session:
        del session['username']
    return redirect('/')


@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        passwordrepeat = request.form['password-repeat']

        collection = mongo.db.users
        user = collection.find_one({'username': username})

        if user == None:
            if password != passwordrepeat:
                flash('Your passwords do not match. Please Try Again')
                return redirect('/register')
            else:
                collection = mongo.db.users
                usersDetails = {'username': username, 'password': password}
                collection.insert_one(usersDetails)
                flash('Successfully registered')
                return redirect(url_for('login'))
        else:
            flash('User Exists Please login')
            return redirect('/register')

    else:
        return render_template('register.html')


@app.route('/community', methods=['GET', 'POST'])
def community():
    collection = mongo.db.communities
    if request.method == 'GET':
        pass

    if request.method == 'POST':
        subject = request.form['subject']
        class_name = request.form['class_name']
        collection.insert_one({'class name': class_name, 'subject': subject, 'posts': []})
        return redirect('/community')

    communities = get_docs(collection)

    return render_template('community.html', communities=communities)


@app.route('/community/<class_code>', methods=['GET', 'POST'])
def view_community(class_code):
    communities = []
    collection = mongo.db.communities

    for x in get_docs(collection):
        communities.append([x['_id'], x['class name']])

    # print(communities)
    for x in communities:
        # print(x)
        if str(x[0]) == str(class_code):
            com_name = str(x[1])

    if request.method == 'POST':
        entry = request.form['entry']
        collection.find_one_and_update({'class name': com_name},
                                       {"$push": {"posts": [uuid.uuid4().hex, session['username'], entry, []]}})
        return redirect('/community/'+class_code)

    all_posts = []
    all_names = []
    sub = collection.find_one({'class name': com_name})['subject']
    post_info = collection.find_one({'class name': com_name})['posts']
    all_ids = []

    for x in post_info:
        all_posts.append(x[2])
        all_names.append(x[1])
        all_ids.append(x[0])

    r = len(all_posts)
    all_names.reverse()
    all_ids.reverse()
    all_posts.reverse()

    return render_template('view_community.html', name=com_name, subject=sub, posts=all_posts,
                           users=all_names, repeat=r, ids=all_ids, class_id=class_code)


@app.route('/community/<class_code>/<post_info>', methods=['GET', 'POST'])
def reply(class_code, post_info):
    info = post_info.split('&')
    collection = mongo.db.communities
    reply_name = []
    reply_post = []
    post_details = collection.find_one({'_id': ObjectId(class_code)})['posts']

    for x in range(len(post_details)):
        if post_details[x][0] == info[0]:
            pos = x

    if request.method == 'GET':
        pass

    if request.method == 'POST':
        entry = request.form['entry']
        collection.find_one_and_update({'_id': ObjectId(class_code)}, {'$push': {'posts.'+str(pos)+'.3': [session['username'], entry]}})
        return redirect(url_for('reply', post_info=post_info, class_code=class_code))

    for x in post_details[pos][3]:
        reply_name.append(x[0])
        reply_post.append(x[1])

    reply_name.reverse()
    reply_post.reverse()
    reply_length = len(reply_post)

    return render_template('comment.html', name=info[1], post=info[2], r_name=reply_name, l=reply_length, r_post=reply_post, code=class_code)


if __name__ == '__main__':
    app.run(debug=True)

