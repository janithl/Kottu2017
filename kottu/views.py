from kottu import app
from kottu.models import Post

@app.route('/')
def index():
	return 'Hello World!'

@app.route('/post/<int:id>/')
def show_post(id):
    post = Post.query.get(id)
    return post.title + ': ' + post.content