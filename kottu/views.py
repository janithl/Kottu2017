from flask import render_template, jsonify
import arrow

from kottu import app
from kottu.models import Post, Blog

PER_PAGE = 20 # items per page

def format_time(timestamp, format=None):
	"""Function to return human-readable/formatted time, then attached to Jinja env"""
	if(format == 'human'):
		return arrow.get(timestamp).humanize()
	else:
		return arrow.get(timestamp).format()

app.jinja_env.filters['format_time'] = format_time

@app.route('/', defaults={'page': 1})
@app.route('/page/<int:page>/')
def index(page):
	"""Renders the front page of Kottu, with all the latest posts"""
	posts = Post.query.order_by(Post.id.desc()).paginate(page, PER_PAGE)
	return render_template('items.html', title='All Posts',
		posts=posts, endpoint='index')

@app.route('/about/')
def about():
	"""Renders the Kottu about page"""
	return render_template('about.html', title='About Kottu')

@app.route('/blogroll/', defaults={'page': 1})
@app.route('/blogroll/page/<int:page>/')
def blogroll(page):
	"""Renders the Kottu blogroll"""
	blogs = Blog.query.order_by(Blog.name.asc()).paginate(page, PER_PAGE * 5)
	return render_template('blogroll.html', title='Kottu Blogroll',
		blogs=blogs, endpoint='blogroll')

@app.route('/blog/<int:id>/', defaults={'page': 1})
@app.route('/blog/<int:id>/page/<int:page>/')
def blog(id, page):
	blog = Blog.query.get(id)
	posts = blog.posts.order_by(Post.id.desc()).paginate(page, PER_PAGE)
	return render_template('items.html', title=blog.name,
		posts=posts, endpoint='blog', blog=blog)