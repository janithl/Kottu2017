import click, feedparser
from time import time as now

from kottu import app
from kottu.models import Post, Blog

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
			click.echo(item.link + ' - ' + item.title)
	else:
		click.echo('Error! Feed returned no items.')