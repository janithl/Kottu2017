import click, feedparser
from time import time as now
from sqlalchemy import exc

from kottu import app
from kottu.models import Post, Blog
from kottu.database import db

@app.cli.command()
def feedget():
	"""Fetch RSS feeds"""
	click.echo('Began feedget')

	blogs = Blog.query.filter(Blog.active == 1) \
		.order_by(Blog.accessed.desc()).limit(20).all()

	for b in blogs:
		fetchandstoreposts(b.id, b.rss)

	return

def fetchandstoreposts(blog_id, blog_rss):
	click.echo('Fetching feed: ' + blog_rss)
	feed = feedparser.parse(blog_rss)
	if(len(feed.entries)):
		click.echo('{} items returned'.format(len(feed.entries)));
		for item in feed.entries:
			post = Post(blog_id, item.link, item.title, 'en', int(now()))
			db.session.add(post)
			try:
				db.session.commit()
				click.echo('Added {} ({}) to database'.format(item.title, item.link))
			except exc.SQLAlchemyError:
				db.session.rollback()
				pass

	else:
		click.echo('Error! Feed returned no items.')