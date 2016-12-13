from flask import render_template, jsonify

from kottu import app
from kottu.models import Post, Blog

PER_PAGE = 20 # items per page

@app.route('/', defaults={'page': 1})
@app.route('/page/<int:page>')
def index(page):
	posts = Post.query.order_by(Post.id.desc()).paginate(page, PER_PAGE)
	return render_template('article.html', title='All Posts', posts=posts)

@app.route('/about/')
def about():
	return render_template('about.html', title='About Kottu')

@app.route('/blog/<int:blog_id>/')
def show_blog_posts(blog_id):
	blog = Blog.query.get_or_404(id)
	return blog.name #render_template('article.html', title=blog.name, posts=blog.posts)