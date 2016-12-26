import click, feedparser, time, re
from sqlalchemy import exc, func

from kottu import app
from kottu.utils import getlang
from kottu.models import Post, Blog
from kottu.database import db

TWO_WEEKS = 2419200 # two weeks in seconds

@app.cli.command()
def feedget():
	"""Fetch RSS feeds"""
	click.echo('Began feedget')

	blog_query = Blog.query.filter(Blog.active == 1) \
		.join(Blog.posts, aliased=True).group_by(Blog.id)

	# get 40 blogs updated in the last two weeks
	updated_blogs = blog_query \
		.having(func.max(Post.timestamp) > time.time() - TWO_WEEKS) \
		.order_by(Blog.accessed.asc()).limit(40)

	# get 60 blogs NOT updated in the last two weeks
	not_updated_blogs = blog_query \
		.having(func.max(Post.timestamp) <= time.time() - TWO_WEEKS) \
		.order_by(Blog.accessed.asc()).limit(60)

	# union them and query
	blogs = updated_blogs.union_all(not_updated_blogs).all()

	for b in blogs:
		if(fetchandstoreposts(b.id, b.rss)):
			b.accessed = int(time.time())
			try:
				db.session.commit()
			except exc.SQLAlchemyError:
				db.session.rollback()

	return

def fetchandstoreposts(blog_id, blog_rss):
	click.echo('Fetching feed: ' + blog_rss)
	feed = feedparser.parse(blog_rss)
	if(len(feed.entries)):
		click.echo('{} items returned'.format(len(feed.entries)));
		for item in feed.entries:
			# we make sure that the post is not "future dated"
			post_time = int(min(time.mktime(item.published_parsed), time.time()))

			# regex to remove html tags, htmlentities and urls
			summary = re.sub("(<[^>]+>|&[^;]+;|(http)s?:\/\/\S+)", "", item.summary).strip()

			post = Post(blog_id, item.link, item.title, summary, 
				getlang(item.title + summary), post_time)
			db.session.add(post)
			try:
				db.session.commit()
				click.echo('Added {} ({}) to database'.format(item.title, item.link))
			except exc.SQLAlchemyError:
				db.session.rollback()
		return True
	else:
		click.echo('Error! Feed returned no items.')
		return False