from . import db
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
from . import login_manager
from datetime import datetime
from sqlalchemy.sql import func

@login_manager.user_loader
def load_user(user_id):
    '''
    @login_manager.user_loader Passes in a user_id to this function
    Function queries the database and gets a user's id as a response
    '''
    return User.query.get(int(user_id))

class User(UserMixin,db.Model):
    '''class modelling the user'''

    __tablename__='users'

    #create the columns
    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(255))
    email = db.Column(db.String(255),unique = True, index =True)
    pasword_hash = db.Column(db.String(255))
    pass_secure = db.Column(db.String(255))
    comment = db.relationship("Comment",backref='user', lazy='dynamic')


    # securing passwords
    @property
    def password(self):
        raise AttributeError('You can not read the password Attribute')

    @password.setter
    def password(self, password):
        self.pass_secure = generate_password_hash(password)

    def verify_password(self,password):
        return check_password_hash(self.pass_secure,password)

    def __repr__(self):
        return f'User {self.username}'

class Blog(db.Model):
    __tablename__ = 'articles'
    id = db.Column(db.Integer,primary_key = True)
    title = db.Column(db.String(255))
    blog = db.Column(db.String(3000))
    comment = db.relationship("Comment",backref='article', lazy='dynamic')

    def save_blog(self):
        '''save a blog in the database'''
        db.session.add(self)
        db.session.commit()

    def delete_blog(self):
        '''delete a given blog from the database'''
        db.session.delete(self)
        db.session.commit()

    # def get_blogs(id):
    #     ''' get all the articles in the database '''
    #     articles = Blog.query.filter_by(id=id).all()
    #     return articles

class Comment(db.Model):
    '''
    Comment class to define the feedback from users
    '''

    # Name of the table
    __tablename__ = 'comments'

    # id column that is the primary key
    id = db.Column(db.Integer, primary_key = True)

    # comment_content for the feedback a user gives to a post
    opinion = db.Column(db.String)

    # post_id column for linking a comment to a specific post
    post_id = db.Column(db.Integer, db.ForeignKey("posts.id",ondelete='CASCADE') )

    # user_id column for linking a comment to a specific user
    user_id = db.Column(db.Integer, db.ForeignKey("users.id") )
