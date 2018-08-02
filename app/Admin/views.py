import os
from . import admin
from .. import db
from flask import render_template, redirect, url_for, flash, session, request,current_app,send_from_directory
from app.Admin.forms import LoginForm,ChangePasswordForm,RoleAddForm,AdminAddForm
from app.models import Admin,Adminlog,Oplog,Role,User,Post,Comment
from functools import wraps


def admin_login_req(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "admin" not in session:
            return redirect(url_for("Admin.login", next=request.url))
        return f(*args, **kwargs)

    return decorated_function


@admin.route("/")
@admin_login_req
def index():
    return render_template('admin/index.html')


@admin.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        data = form.data
        admin = Admin.query.filter_by(name=data["account"]).first()
        if admin is not None and admin.verify_password(form.pwd.data):
            session["admin"] = data["account"]
            adminlogs=Adminlog(
                ip=request.environ['REMOTE_ADDR'],
                admin=admin)
            db.session.add(adminlogs)
            return redirect(request.args.get("next") or url_for("Admin.index"))
        flash('用户名或密码错误')
    return render_template("admin/login.html", form=form)


@admin.route("/logout")
@admin_login_req
def logout():
    session.pop("admin", None)
    return redirect(url_for('Admin.login'))


@admin.route("/pwd",methods=['GET','POST'])
@admin_login_req
def pwd():
    form=ChangePasswordForm()
    if form.validate_on_submit():
        admin=Admin.query.filter_by(name=session["admin"]).first()
        if admin.verify_password(form.old_password.data):
            admin.password=form.password.data
            adminOplog=Oplog(
                reason='修改密码',
                ip=request.environ['REMOTE_ADDR'],
                admin=admin)
            db.session.add(adminOplog)
            db.session.add(admin)
            flash('密码已更改')
            return redirect(url_for("Admin.pwd"))
    return render_template('admin/pwd.html',form=form)

@admin.route("/user/list")
@admin_login_req
def user_list():
    page = request.args.get('page', 1, type=int)
    pagination = User.query.order_by(User.addtime).paginate(
        page, per_page=current_app.config['FLASKY_USERS_PER_PAGE'],
        error_out=False)
    users = pagination.items
    return render_template('admin/user_list.html',
        users=users,pagination=pagination)

@admin.route("/delete_user/<int:id>",methods=['GET','POST'])
@admin_login_req
def delete_user(id):
    user=User.query.get_or_404(id)
    for post in user.posts:
        db.session.delete(post)
    current_admin=Admin.query.filter_by(name=session["admin"]).first()
    adminOplog=Oplog(
        reason='删除用户',
        ip=request.environ['REMOTE_ADDR'],
        admin=current_admin)
    db.session.add(adminOplog)
    db.session.delete(user)    
    return redirect(url_for('.user_list'))

@admin.route("/post/list")
@admin_login_req
def post_list():
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.order_by(Post.timestamp.desc()).paginate(
        page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
        error_out=False)
    posts = pagination.items
    return render_template('admin/post_list.html',
        posts=posts,pagination=pagination)

@admin.route("/delete_post/<int:id>",methods=['GET','POST'])
@admin_login_req
def delete_post(id):
    post=Post.query.get_or_404(id)
    current_admin=Admin.query.filter_by(name=session["admin"]).first()
    adminOplog=Oplog(
        reason='删除post',
        ip=request.environ['REMOTE_ADDR'],
        admin=current_admin)
    comments=post.comments
    for comment in comments:
        comment = Comment.query.filter_by(id=comment.id).first()
        db.session.delete(comment)
    db.session.add(adminOplog)
    db.session.delete(post)    
    return redirect(url_for('.post_list'))    

@admin.route("/comment/list")
@admin_login_req
def comment_list():
    page = request.args.get('page', 1, type=int)
    pagination = Comment.query.order_by(Comment.timestamp.desc()).paginate(
        page, per_page=current_app.config['FLASKY_COMMENTS_PER_PAGE'],
        error_out=False)
    comments = pagination.items
    return render_template('admin/comment_list.html',
        comments=comments,pagination=pagination)

@admin.route("/delete_comment/<int:id>",methods=['GET','POST'])
@admin_login_req
def delete_comment(id):
    comment=Comment.query.get_or_404(id)
    current_admin=Admin.query.filter_by(name=session["admin"]).first()
    adminOplog=Oplog(
        reason='删除评论',
        ip=request.environ['REMOTE_ADDR'],
        admin=current_admin)
    db.session.add(adminOplog)
    db.session.delete(comment)    
    return redirect(url_for('.comment_list'))    

@admin.route("/file/list")
@admin_login_req
def file_list():
    files = [f for f in os.listdir(current_app.config['UPLOAD_FOLDER'])if os.path.isfile(os.path.join(current_app.config['UPLOAD_FOLDER'],f))]
    files_list = []
    for f in files:
        size = os.path.getsize(os.path.join(current_app.config['UPLOAD_FOLDER'], f))/1024
        files_list.append({'name': f,'size':int(size),'url':'/file/'+f,'thumb_url':'/thumb_file/'+f,'delete_url':'/delete/'+f})
    url_root=request.url_root
    return render_template('admin/file_list.html',url_root=url_root,files_list=files_list)

@admin.route("/file/<string:filename>", methods=['GET'])
@admin_login_req
def get_file(filename):
    return send_from_directory(os.path.join(current_app.config['UPLOAD_FOLDER']), filename=filename)

@admin.route("/thumb_file/<string:filename>", methods=['GET'])
@admin_login_req
def get_thumb_file(filename):
    return send_from_directory(os.path.join(current_app.config['THUMBNAIL_FOLDER']), filename=filename)    

@admin.route("/delete/<string:filename>", methods=['GET','POST'])
@admin_login_req
def delete(filename):
    file_path = os.path.join(current_app.config['UPLOAD_FOLDER'],filename)
    file_thumb_path = os.path.join(current_app.config['THUMBNAIL_FOLDER'],filename)
    if os.path.exists(file_path):
        try:
            current_admin=Admin.query.filter_by(name=session["admin"]).first()
            adminOplog=Oplog(
                reason='删除文件',
                ip=request.environ['REMOTE_ADDR'],
                admin=current_admin)
            db.session.add(adminOplog)
            if os.path.exists(file_thumb_path):
                os.remove(file_thumb_path)
            os.remove(file_path)
            return redirect(url_for('.file_list'))
        except:
            return redirect(url_for('.file_list'))      

@admin.route("/oplog/list")
@admin_login_req
def oplog_list():
    page = request.args.get('page', 1, type=int)
    pagination = Oplog.query.order_by(Oplog.addtime.desc()).paginate(
        page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
        error_out=False)
    oplogs = pagination.items
    admin=Admin.query.filter_by(name=session['admin']).first()
    return render_template('admin/oplog_list.html',
        oplogs=oplogs,pagination=pagination,admin=admin)

@admin.route("/delete_oplog/<int:id>",methods=['GET','POST'])
@admin_login_req
def delete_oplog(id):
    oplog=Oplog.query.get_or_404(id)
    admin=Admin.query.filter_by(name=session['admin']).first()
    if admin.role.name=='超级管理员':
        adminOplog=Oplog(
            reason='删除操作log',
            ip=request.environ['REMOTE_ADDR'],
            admin=admin)
        db.session.add(adminOplog)
        db.session.delete(oplog)
        return redirect(url_for('.oplog_list'))
    else:
        return redirect(url_for('.oplog_list'))

@admin.route("/adminlog/list")
@admin_login_req
def adminlog_list():
    page = request.args.get('page', 1, type=int)
    pagination = Adminlog.query.order_by(Adminlog.addtime.desc()).paginate(
        page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
        error_out=False)
    adminlogs = pagination.items
    admin=Admin.query.filter_by(name=session['admin']).first()
    return render_template('admin/adminlog_list.html',
        adminlogs=adminlogs,pagination=pagination,admin=admin)

@admin.route("/delete_adminlog/<int:id>",methods=['GET','POST'])
@admin_login_req
def delete_adminlog(id):
    adminlog=Adminlog.query.get_or_404(id)
    admin=Admin.query.filter_by(name=session['admin']).first()
    if admin.role.name=='超级管理员':
        adminOplog=Oplog(
            reason='删除adminlog',
            ip=request.environ['REMOTE_ADDR'],
            admin=admin)
        db.session.add(adminOplog)
        db.session.delete(adminlog)
        return redirect(url_for('.adminlog_list'))
    else:
        return redirect(url_for('.adminlog_list'))

@admin.route("/role/add",methods=['GET','POST'])
@admin_login_req
def role_add():
    form=RoleAddForm()
    if form.validate_on_submit():
        data=form.data
        admin=Admin.query.filter_by(name=session["admin"]).first()
        check_role=Role.query.filter_by(name=data['role']).first()
        if check_role is None:
            role=Role(
                name=data['role']
                )
            adminOplog=Oplog(
                    reason='添加角色',
                    ip=request.environ['REMOTE_ADDR'],
                    admin=admin)
            db.session.add(adminOplog)
            db.session.add(role)
            flash('角色已添加')
            return redirect(url_for("Admin.role_add"))
        else:    
            flash('角色名已存在')
            return redirect(url_for("Admin.role_add"))
    return render_template('admin/role_add.html',form=form)

@admin.route("/role/list")
@admin_login_req
def role_list():
    current_admin=Admin.query.filter_by(name=session["admin"]).first()
    page = request.args.get('page', 1, type=int)
    pagination = Role.query.order_by(Role.addtime).paginate(
        page, per_page=current_app.config['FLASKY_USERS_PER_PAGE'],
        error_out=False)
    roles = pagination.items
    return render_template('admin/role_list.html',
        roles=roles,current_admin=current_admin,pagination=pagination)

@admin.route("/delete_role/<int:id>",methods=['GET','POST'])
@admin_login_req
def delete_role(id):
    role=Role.query.get_or_404(id)
    current_admin=Admin.query.filter_by(name=session["admin"]).first()
    if current_admin.role.name=='超级管理员':
        adminOplog=Oplog(
            reason='删除角色',
            ip=request.environ['REMOTE_ADDR'],
            admin=current_admin)
        db.session.add(adminOplog)
        db.session.delete(role)    
        return redirect(url_for('.role_list'))
    else:
        return redirect(url_for('.role_list'))            

@admin.route("/admin/add",methods=['GET','POST'])
@admin_login_req
def admin_add():
    form=AdminAddForm()
    if form.validate_on_submit():
        data=form.data
        admin=Admin.query.filter_by(name=session["admin"]).first()
        check_admin=Admin.query.filter_by(name=data['adminname']).first()
        role=Role.query.filter_by(name=data['roletype']).first()
        if admin.role==None:
            flash('您没有添加权限')
            return redirect(url_for("Admin.admin_add"))
        if admin.role.name!='超级管理员':
            flash('您没有添加权限')
            return redirect(url_for("Admin.admin_add"))
        elif check_admin is None and admin.role.name=='超级管理员':
            add_admin=Admin(
                name=data['adminname'],
                password=data['password'],
                role=role)
            adminOplog=Oplog(
                    reason='添加管理员',
                    ip=request.environ['REMOTE_ADDR'],
                    admin=admin)
            db.session.add(adminOplog)
            db.session.add(add_admin)
            flash('管理员已添加')
            return redirect(url_for("Admin.admin_add"))
        else:    
            flash('管理员昵称已存在')
            return redirect(url_for("Admin.admin_add"))
    return render_template('admin/admin_add.html',form=form)

@admin.route("/admin/list")
@admin_login_req
def admin_list():
    page = request.args.get('page', 1, type=int)
    pagination = Admin.query.order_by(Admin.addtime).paginate(
        page, per_page=current_app.config['FLASKY_USERS_PER_PAGE'],
        error_out=False)
    admins = pagination.items
    current_admin=Admin.query.filter_by(name=session["admin"]).first()
    return render_template('admin/admin_list.html',
        admins=admins,current_admin=current_admin,pagination=pagination)

@admin.route("/delete_admin/<int:id>",methods=['GET','POST'])
@admin_login_req
def delete_admin(id):
    admin=Admin.query.get_or_404(id)
    current_admin=Admin.query.filter_by(name=session["admin"]).first()
    adminOplog=Oplog(
        reason='删除管理员',
        ip=request.environ['REMOTE_ADDR'],
        admin=current_admin)
    db.session.add(adminOplog)
    db.session.delete(admin)    
    return redirect(url_for('.admin_list'))    