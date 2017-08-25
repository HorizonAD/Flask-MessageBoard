from datetime import datetime
import hashlib,bleach
from markdown import markdown
from flask_login import UserMixin,AnonymousUserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app, request, url_for
from app.exceptions import ValidationError
from . import db,login_manager

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    avatar = db.Column(db.String(128),default=None)
    location = db.Column(db.String(64))
    about_me = db.Column(db.Text())
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    comments = db.relationship('Comment', backref='author', lazy='dynamic')

    @staticmethod
    def generate_fake(count=100):
        from sqlalchemy.exc import IntegrityError
        from random import seed
        import forgery_py  #生成虚拟数据所需要的库

        seed()
        for i in range(count):
            u = User(username=forgery_py.internet.user_name(True),
                    location=forgery_py.address.city(),
                    about_me=forgery_py.lorem_ipsum.sentence(),
                    password=forgery_py.lorem_ipsum.word())
            db.session.add(u)
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()
                
    #设置该属性不可读
    @property
    def password(self):
        raise AttributeError('password不可读')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User %r>' % self.username

class AnonymousUser(AnonymousUserMixin):
    def __init__(self):
        self.username = '游客'

login_manager.anonymous_user = AnonymousUser

@login_manager.user_loader
def load_user(userid):
    return User.query.get(int(userid))

class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    body_html = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    comments = db.relationship('Comment', backref='post', lazy='dynamic')

    @staticmethod
    def generate_fake(count=100):
        from random import seed, randint
        import forgery_py

        seed()
        user_count = User.query.count()
        for i in range(count):
            u = User.query.offset(randint(0, user_count - 1)).first()
            p = Post(body=forgery_py.lorem_ipsum.sentences(randint(1, 5)),
                     timestamp=forgery_py.date.date(True),
                     author=u)
            db.session.add(p)
            db.session.commit()

    #处理富文本，将Markdown格式转换为Html
    @staticmethod
    def on_changed_body(target, value, oldvalue, initiator):
        allowed_tags = ['a', 'abbr', 'acronym', 'b', 'blockquote', 'code',
                        'em', 'i', 'li', 'ol', 'pre', 'strong', 'ul',
                        'h1', 'h2', 'h3', 'p']
        target.body_html = bleach.linkify(bleach.clean(
            markdown(value, output_format='html'),
            tags=allowed_tags, strip=True))


db.event.listen(Post.body, 'set', Post.on_changed_body)

class Follow(db.Model):
    __tablename__ = 'follows'
    follower_id = db.Column(db.Integer, db.ForeignKey('comments.id'),
                           primary_key=True)
    followed_id = db.Column(db.Integer, db.ForeignKey('comments.id'),
                         primary_key=True)

class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    body_html = db.Column(db.Text)
    anonymoususer=db.Column(db.String(64))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))
    comment_type = db.Column(db.String(64), default='comment')
    reply_to = db.Column(db.String(128), default='notReply')
    followed = db.relationship('Follow',
                               foreign_keys=[Follow.follower_id],
                               backref=db.backref('follower', lazy='joined'),
                               lazy='dynamic',
                               cascade='all, delete-orphan')
    followers = db.relationship('Follow',
                               foreign_keys=[Follow.followed_id],
                               backref=db.backref('followed', lazy='joined'),
                               lazy='dynamic',
                               cascade='all, delete-orphan')
    @staticmethod
    def generate_fake(count=100):
        from random import seed, randint
        import forgery_py

        seed()
        post_count = Post.query.count()
        for i in range(count):
            a = Post.query.offset(randint(0, post_count - 1)).first()
            c = Comment(body=forgery_py.lorem_ipsum.sentences(randint(3, 5)),
                        timestamp=forgery_py.date.date(True),
                        post=a)
            db.session.add(c)
        try:
            db.session.commit()
        except:
            db.session.rollback()

    @staticmethod
    def generate_fake_replies(count=100):
        from random import seed, randint
        import forgery_py

        seed()
        comment_count = Comment.query.count()
        for i in range(count):
            followed = Comment.query.offset(randint(0, comment_count - 1)).first()
            c = Comment(body=forgery_py.lorem_ipsum.sentences(randint(3, 5)),
                        timestamp=forgery_py.date.date(True),
                        post=followed.post, comment_type='reply',
                        reply_to=followed.author)
            f = Follow(follower=c, followed=followed)
            db.session.add(f)
            db.session.commit()

    @staticmethod
    def on_changed_body(target, value, oldvalue, initiator):
        allowed_tags = ['a', 'abbr', 'acronym', 'b', 'code', 'em', 'i',
                        'strong']
        target.body_html = bleach.linkify(bleach.clean(
            markdown(value, output_format='html'),
            tags=allowed_tags, strip=True))

    def is_reply(self):
        if self.followed.count() == 0:
            return False
        else:
            return True
    # to confirm whether the comment is a reply or not 

    def followed_name(self):
        if self.is_reply():
            return self.followed.first().followed.author         

db.event.listen(Comment.body, 'set', Comment.on_changed_body)