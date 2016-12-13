from flask import request, redirect, render_template
import arrow

from kottu import app
from kottu.models import Post, Blog

PER_PAGE = 20 # items per page

@app.template_filter('format_time')
def format_time(timestamp, format=None):
	"""Jinja filter to return human-readable/formatted time"""
	if(format == 'human'):
		return arrow.get(timestamp).humanize()
	else:
		return arrow.get(timestamp).format()

@app.route('/', defaults={'page': 1})
@app.route('/page/<int:page>/')
def index(page):
	"""Renders the front page of Kottu, with all the latest posts"""
	posts = Post.query.order_by(Post.id.desc()).paginate(page, PER_PAGE)
	return render_template('items.html', title='All Posts',
		posts=posts, endpoint='index')

@app.route('/go/')
def go():
	"""Implements /go/?id={}&url={}, which tracks clicks"""
	return redirect(request.args.get('url'))

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

@app.route('/blog/<int:id>/', defaults={'page': 1, 'popular': None})
@app.route('/blog/<int:id>/<popular>', defaults={'page': 1})
@app.route('/blog/<int:id>/page/<int:page>/', defaults={'popular': None})
@app.route('/blog/<int:id>/<popular>/page/<int:page>/')
def blog(id, popular, page):
	blog = Blog.query.get(id)
	if(popular):
		posts = blog.posts.order_by(Post.buzz.desc())
	else:
		posts = blog.posts.order_by(Post.id.desc())
	posts = posts.paginate(page, PER_PAGE)

	return render_template('items.html', title=blog.name,
		posts=posts, endpoint='blog', blog=blog, popular=popular)