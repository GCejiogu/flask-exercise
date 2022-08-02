
import os
from flask import Flask,render_template,url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy.sql import func
from sqlalchemy import text
from flask_migrate import Migrate



app=Flask(__name__)
db = SQLAlchemy(app)
migrate=Migrate(app,db)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/Entertainment', methods = ['GET'])
def Entertainment():
    return render_template('Entertainment')

@app.route('/Sports', methods=['POST'])
def Sports():
    return render_template('Sports')

@app.route('/Health', methods=['POST'])
def Health ():
    return render_template('Health')




class Author (db.Model):
    id = db.Column(db.Integer,primary_key=True)
    profile=db.Column(db.Text,nullable=False)
    no_of_post=db.Column(db.Integer,nullable=False)
    follower=db.Column(db.Integer,nullable=True)

    def __init__(self, id:int, profile:str, no_of_post:str, follower:str):
        self.id = id
        self.profile = profile
        self.no_of_post = no_of_post
        self.follower = follower
    
    def serialize(self):
        return {
            'id': self.id,
            'profile': self.profile,
            'no_of_post': self.no_of_post,
            'follower': self.follower
        }
    
    def __repr__(self):
        return '<Author%r>' % self.profile

    


class Post (db.Model):
    id=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String,nullable=False)
    date_posted=db.Column(db.DateTime,nullable=False)
    like=db.Column(db.Integer,nullable=True)
    dislike=db.Column(db.Integer,nullable=True)
    body=db.Column(db.Text,nullable=False)
    comment= db.Column(db.Text,nullable=True)

    author_id=db.Column(db.Integer,db.ForeignKey('author.id'), nullable =False)
    author=db.relationship('Author', backref=db.backref('posts',lazy=True))

    category_id=db.Column(db.Integer,db.ForeignKey('category.id'),nullable=False)
    category=db.relationship('Category', backref=db.backref('posts',lazy=True))

    def __init__(self, title:str, date_posted:datetime, like:int, dislike:int, body:str, comment:str):
        self.title = title
        self.date_posted = date_posted
        self.like = like
        self.dislike = dislike
        self.body = body
        self.comment = comment

    
    def serialize(self):
        return{
        'id': self.id,
        'title':self.title,
        'date_posted':self.date_posted.isoformat(),
        'like': self.like,
        'dislike': self.dislike,
        'body': self.body,
        'comment': self.comment,
        'autho_id': self.author_id,
        'category_id':self.category_id

        }


    def __repr__(self):
        return '<Post%r>' % self.title




class Category(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String,nullable=False)
    

    def __init__ (self,name:str):
        self.name = name


    def serialize(self):
        return {
        'id': self.id,
        'name':self.name
    }

    def __repr__(self):
        return '<Category%r>' % self.name


if __name__ =='__main__':

    app.run(debug=True)


