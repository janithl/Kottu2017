from flask import render_template, jsonify

from kottu import app
from kottu.models import Post, Blog

PER_PAGE = 20 # items per page

@app.route('/', defaults={'page': 1})
@app.route('/page/<int:page>/')
def index(page):
	"""Renders the front page of Kottu, with all the latest posts"""
	posts = Post.query.order_by(Post.id.desc()).paginate(page, PER_PAGE)
	return render_template('article.html', title='All Posts', posts=posts)

@app.route('/about/')
def about():
	"""Renders the Kottu about page"""
	return render_template('about.html', title='About Kottu')

@app.route('/blogroll/', defaults={'page': 1})
@app.route('/blogroll/page/<int:page>/')
def blogroll(page):
	"""Renders the Kottu blogroll"""
	blogs = Blog.query.order_by(Blog.name.asc()).paginate(page, PER_PAGE * 5)
	return render_template('blogroll.html', title='Blogroll', blogs=blogs)

@app.route('/blog/<int:blog_id>/')
def blog(blog_id):
	blog = Blog.query.get_or_404(id)
	return blog.name #render_template('article.html', title=blog.name, posts=blog.posts)