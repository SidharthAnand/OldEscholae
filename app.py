from flask import*
from models import*

#add the security lines here
app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():

    if request.method == 'GET':
        pass

    if request.method == 'POST':
        name = request.form.get('name')
        post = request.form.get('post')
        create_post(name, post)
        print('post created ')

    posts = get_post()

    return render_template('index.html', posts=posts)


if __name__ == '__main__':
    app.run(debug=True)

