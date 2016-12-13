from flask import render_template, jsonify

from kottu import app
from kottu.models import Post, Blog

@app.route('/')
def index():
	posts = Post.query.order_by(Post.id.desc()).paginate()
	return render_template('article.html', title='All Posts', posts=posts)

@app.route('/blog/<int:blog_id>/')
def show_blog_posts(blog_id):
	blog = Blog.query.get_or_404(id)
	return blog.name #render_template('article.html', title=blog.name, posts=blog.posts)