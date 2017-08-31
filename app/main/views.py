import os,hashlib
from werkzeug.utils import secure_filename
from flask import render_template, redirect, url_for, abort, flash, request,current_app, make_response,send_from_directory
from flask_login import login_required, current_user
from flask_sqlalchemy import get_debug_queries
from . import main
from datetime import datetime
from .forms import EditProfileForm, CommentForm,PostForm,UploadForm,AnonymousCommentForm
from .. import db
from ..models import User, Post, Comment,Follow
from ..email import send_email

@main.after_app_request
def after_request(response):
    for query in get_debug_queries():
        if query.duration >= current_app.config['FLASKY_SLOW_DB_QUERY_TIME']:
            current_app.logger.warning(
                'Slow query: %s\nParameters: %s\nDuration: %fs\nContext: %s\n'
                % (query.statement, query.parameters, query.duration,
                   query.context))
    return response

@main.route('/', methods=['GET', 'POST'])
def index():
    form = PostForm()
    if current_user.is_anonymous and form.validate_on_submit():
        flash('游客不能提交哦')
        return redirect(url_for('.index'))
    if current_user._get_current_object() and form.validate_on_submit():
            post = Post(body=form.body.data,
                        author=current_user._get_current_object())
            db.session.add(post)
            send_email('328588917@qq.com', '新吐槽',
                   'auth/email/notice', 
                   post_id=post.id,
                   user=current_user._get_current_object())
            flash('槽点已发布')
            return redirect(url_for('.index'))
    page = request.args.get('page', 1, type=int)
    query = Post.query
    pagination = query.order_by(Post.timestamp.desc()).paginate(
        page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
        error_out=False)
    posts = pagination.items
    return render_template('index.html',form=form, posts=posts, pagination=pagination)

@main.route('/searchpost')
def searchpost():
    form = PostForm()
    q=request.args.get('q')
    search_post_result=Post.query.filter(Post.body.contains(q))
    if search_post_result.all():
        return render_template('index.html',form=form,posts=search_post_result)
    else:
        flash('未搜到相应关键字')
        return render_template('index.html',form=form)

@main.route('/searchcomment')
def searchcomment():
    form = PostForm()
    q=request.args.get('q')
    search_comment_result=Comment.query.filter(Comment.body.contains(q))
    if search_comment_result.all():
        path=request.path
        return render_template('comment.html',path=path,comments=search_comment_result)
    else:
        flash('未搜到相应关键字')
        return render_template('index.html',form=form)        

@main.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first()
    page = request.args.get('page', 1, type=int)
    posts_pagination = user.posts.order_by(Post.timestamp.desc()).paginate(
        page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
        error_out=False)
    posts = posts_pagination.items
    comments_pagination = user.comments.order_by(Comment.timestamp.asc()).paginate(
            page, per_page=current_app.config['FLASKY_COMMENTS_PER_PAGE'],
            error_out=False)
    comments = comments_pagination.items
    path=request.path
    return render_template('user.html', user=user, 
        posts=posts,posts_pagination=posts_pagination,
        comments=comments,comments_pagination=comments_pagination,path=path)


@main.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.username = form.name.data
        current_user.location = form.location.data
        current_user.about_me = form.about_me.data
        db.session.add(current_user)
        flash('个人信息已更新')
        return redirect(url_for('.user', username=current_user.username))
    form.name.data = current_user.username
    form.location.data = current_user.location
    form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', form=form)

@main.route('/comment', methods=['GET', 'POST'])
def comments():
    page = request.args.get('page', 1, type=int)
    pagination = Comment.query.order_by(Comment.timestamp.asc()).paginate(
            page, per_page=current_app.config['FLASKY_COMMENTS_PER_PAGE'],
            error_out=False)
    comments = pagination.items
    path=request.path
    url_root=request.url_root.rstrip('/')
    return render_template('comment.html',path=path,url_root=url_root,comments=comments,pagination=pagination)    

@main.route('/post/<int:id>', methods=['GET', 'POST'])
def post(id):
    post = Post.query.get_or_404(id)
    if not current_user._get_current_object():
        abort(403)
    elif current_user.is_anonymous:
        form=AnonymousCommentForm()
        if form.validate_on_submit():
            comment = Comment(body=form.body.data,
                              post=post,
                              anonymoususer=form.name.data)
            db.session.add(comment)
            followed_id = int(form.follow.data)
            if followed_id != -1:
                followed = Comment.query.get_or_404(followed_id)
                f = Follow(follower=comment, followed=followed)
                comment.comment_type = 'reply'
                if followed.author is None:
                    comment.reply_to = followed.anonymoususer
                else:
                    comment.reply_to = followed.author.username
                db.session.add(f)
                db.session.add(comment)
            send_email('328588917@qq.com', '新评论',
                   'auth/email/notice')    
            flash('评论已发布')
            return redirect(url_for('.post', id=post.id, page=-1))
    else:
        form = CommentForm()
        if form.validate_on_submit():
            comment = Comment(body=form.body.data,
                              post=post,
                              author=current_user._get_current_object())
            db.session.add(comment)
            followed_id = int(form.follow.data)
            if followed_id != -1:
                followed = Comment.query.get_or_404(followed_id)
                f = Follow(follower=comment, followed=followed)
                comment.comment_type = 'reply'
                if followed.author is None:
                    comment.reply_to = followed.anonymoususer
                else:
                    comment.reply_to = followed.author.username
                db.session.add(f)
                db.session.add(comment)
            send_email('328588917@qq.com', '新评论',
                   'auth/email/notice')    
            flash('评论已发布')
            return redirect(url_for('.post', id=post.id, page=-1))
    page = request.args.get('page', 1, type=int)
    if page == -1:
        page = (post.comments.count() - 1) // \
            current_app.config['FLASKY_COMMENTS_PER_PAGE'] + 1
    pagination = post.comments.order_by(Comment.timestamp.asc()).paginate(
        page, per_page=current_app.config['FLASKY_COMMENTS_PER_PAGE'],
        error_out=False)
    comments = pagination.items
    return render_template('post.html', posts=[post], form=form,
                           comments=comments,id=post.id, pagination=pagination)

@main.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    post = Post.query.get_or_404(id)
    if current_user != post.author and \
            not current_user._get_current_object():
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.body = form.body.data
        db.session.add(post)
        flash('槽点已更新')
        return redirect(url_for('.post', id=post.id))
    form.body.data = post.body
    return render_template('edit_post.html', form=form)

@main.route('/delete_comment/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_comment(id):
    comment = Comment.query.get_or_404(id)
    if current_user != comment.author and \
            not current_user._get_current_object():
        abort(403)
    else:
        post_id=comment.post.id
        db.session.delete(comment)
        flash('评论已删除')
        return redirect(url_for('.post',id=post_id))

@main.route('/delete_post/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_post(id):
    post = Post.query.get_or_404(id)
    if current_user != post.author and \
            not current_user._get_current_object():
        abort(403)
    else:
        username=post.author.username
        comments=post.comments
        for comment in comments:
            comment = Comment.query.filter_by(id=comment.id).first()
            db.session.delete(comment)
        db.session.delete(post)
        flash('槽点已删除')
        return redirect(url_for('.user',username=username))        

@main.route('/all')
@login_required
def show_all():
    resp = make_response(redirect(url_for('.index')))
    return resp

@main.route('/avatar/<filename>')
def get_file(filename):
    return send_from_directory(current_app.config['UPLOAD_FOLDER'],filename)    

@main.route('/upload_file',methods = ['GET','POST'])
@login_required
def upload_file():
    form = UploadForm()
    if request.method == 'POST':
        file = request.files['image']
        if file:
            filename = secure_filename(file.filename)
            if not filename.rsplit('.',1)[1] in current_app.config['ALLOWED_EXTENSIONS']:
                flash('文件格式错误')
                return redirect(url_for('.upload_file'))
            nowtime = datetime.now()
            #重命名,format字符串格式化
            filename = hashlib.md5('{0}_{1}'.format(filename,nowtime).encode("gb2312")).hexdigest()+"."+filename.rsplit('.',1)[1]
            file.save(os.path.join(current_app.config['UPLOAD_FOLDER'],filename))
            if current_user.avatar:
                try:
                    os.remove(os.path.join(current_app.config['UPLOAD_FOLDER'],current_user.avatar))
                except OSError:
                    return {"error": u'文件不存在'}
            current_user.avatar=filename
            flash('头像已更改')
            return redirect(url_for('.user', username=current_user.username))
        else: #似乎多余，但可以验证直接post
            flash('未选择文件')
            return redirect(url_for('.upload_file'))
    return render_template('upload_file.html', form=form)  