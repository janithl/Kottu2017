from kottu import app
from kottu.database import db

class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column('postID', db.Integer, primary_key=True)
    title = db.Column(db.String(192))
    content = db.Column('postContent', db.String)

    def __init__(self):
        pass

    def __repr__(self):
        return '<Post %r>' % self.title