from kottu import app
from kottu.database import db

class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column('postID', db.Integer, primary_key=True)
    blog_id = db.Column('blogID', db.Integer)
    link = db.Column(db.String(320))
    title = db.Column(db.String(192))
    content = db.Column('postContent', db.String)
    thumbnail = db.Column(db.String(128))
    language = db.Column(db.String(2))
    timestamp = db.Column('serverTimestamp', db.Integer)
    fbcount = db.Column(db.Integer)
    buzz = db.Column('postBuzz', db.Float)
    trend = db.Column(db.Float)

    def __init__(self):
        pass

    def __repr__(self):
        return '<Post %r>' % self.title

class Blog(db.Model):
    __tablename__ = 'blogs'
    id = db.Column('bid', db.Integer, primary_key=True)
    name = db.Column('blogName', db.String(64))
    url = db.Column('blogURL', db.String(64))
    rss = db.Column('blogRSS', db.String(128))
    accessed = db.Column('access_ts', db.Integer)
    active = db.Column(db.Integer)
    posts = db.relationship('Post', backref='blog',
        primaryjoin='Post.blog_id==Blog.id',
        foreign_keys='Post.blog_id', lazy='dynamic')
