from kottu import app
from kottu.database import db

class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column('postID', db.Integer, primary_key=True)
    title = db.Column(db.String(192))
    link = db.Column(db.String(320))
    content = db.Column('postContent', db.String)
    blog_id = db.Column('blogID', db.Integer)

    def __init__(self):
        pass

    def __repr__(self):
        return '<Post %r>' % self.title

class Blog(db.Model):
    __tablename__ = 'blogs'
    id = db.Column('bid', db.Integer, primary_key=True)
    name = db.Column('blogName', db.String(64))
    url = db.Column('blogURL', db.String(64))
    posts = db.relationship('Post', backref='blog',
        primaryjoin='Post.blog_id==Blog.id',
        foreign_keys='Post.blog_id', lazy='dynamic')
