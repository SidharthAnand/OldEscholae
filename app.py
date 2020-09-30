from flask import*
from models import *
import flask_bootstrap
from flask_pymongo import PyMongo
from pymongo import *
import bcrypt

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
        collection.find_one_and_update({'class name': com_name}, {"$push": {"posts": entry}})
        return redirect('/community/'+class_code)

    sub = collection.find_one({'class name': com_name})['subject']
    all_posts = reversed(collection.find_one({'class name': com_name})['posts'])

    return render_template('view_community.html', name=com_name, subject=sub, posts=all_posts)


if __name__ == '__main__':
    app.run(debug=True)

