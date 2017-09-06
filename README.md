# MessageBoard(python3.6+flask+Bootstrap3)
演示：(不久可能会失效)[吐点槽吧](http://liuyan.flywinky.top/)

# 本地预览
- clone到本地
```
git clone https://github.com/bayi27/flask-MessageBoard.git
```
- 虚拟环境
```
vitualenv venv

C:\Users\bayi\Desktop\message
(venv) λ pip install requirements.txt #虚拟环境中
```

- 生成数据库并添加管理员(角色自定)
```
C:\Users\bayi\Desktop\message
(venv) λ python manage.py shell
>>> db.create_all()
>>> admin=Admin(name='八一',password='12345')
>>> db.session.add(admin)
>>> db.session.commit()
```
- 运行
```
C:\Users\bayi\Desktop\message
(venv) λ ppython manage.py runserver
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 273-960-183
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
```
		
# 项目结构
```
|- app
	|- Admin
		|- __init__.py
		|- forms.py
		|- views.py
	|- auth 用户模块
		|- __init__.py
		|- forms.py
		|- views.py
	|- main 
		|- __init__.py
		|- errors.py
		|- forms.py
		|- views.py
	|- satatic
		|- css
			|- style.css
		|- images
			|- admin.gif
			|- favicon.gif
		|- js
			|- comment.js
			|- search.js
	|- templates
		|- admin
			|- admin.html
		|- auth 用户
			|- change_password.html 
			|- login.html
			|- register.html
		|- 403.html
		|- 404.html
		|- 500.html
		|- _comments.html
		|- _macros.html
		|- _posts.html
		|- base.html
		|- edit_post.html
		|- edit_profile.html
		|- error_page.html
		|- index.html
		|- post.html
		|- upload_file.html
		|- user.html
	|- upload 文件上传
		|- avatar 用户头像
			|- thumbnail 缩略图
	|- __init__.py 初始化app文件
	|- email.py email配置以及异步实现
	|- exceptions.py
	|- admin.py
	|- models.py 数据库模型	
|- migrations 数据库迁移文件	
|- config.py 配置文件
|- manage.py run文件
```

# 后端考核任务

《吐槽》

根据狗书假期修改版

- 增加头像自定义,文件上传部分可拓展

- 增加一问一答形式回复功能,游客功能以及游客评论不能发布吐槽

- 增加新评论邮件推送管理员

- 增加首页搜索功能以及comment路由

- 增加admin模块(使用flask-admin插件)

- 结合bootstrap3,自定义后台[https://adminlte.io/premium](https://adminlte.io/premium)

- 文件浏览前端样式[https://github.com/blueimp/jQuery-File-Upload](https://github.com/blueimp/jQuery-File-Upload)

![演示](http://on2mh1s1f.bkt.clouddn.com/QQ%E6%88%AA%E5%9B%BE20170906153214.png?imageView2/0/q/75|watermark/2/text/5YWr5LiA/font/5b6u6L2v6ZuF6buR/fontsize/600/fill/I0U5MjQyNA==/dissolve/100/gravity/SouthEast/dx/10/dy/10|imageslim)

# 所有url
可以使用python manage.py showurls生成
```
/                                             main.index
/6oPT/                                        admin.index
/6oPT/comment/                                comment.index_view
/6oPT/comment/action/                         comment.action_view
/6oPT/comment/ajax/lookup/                    comment.ajax_lookup
/6oPT/comment/ajax/update/                    comment.ajax_update
/6oPT/comment/delete/                         comment.delete_view
/6oPT/comment/details/                        comment.details_view
/6oPT/comment/edit/                           comment.edit_view
/6oPT/comment/export/<export_type>/           comment.export
/6oPT/comment/new/                            comment.create_view
/6oPT/fileadmin/                              fileadmin.index_view
/6oPT/fileadmin/action/                       fileadmin.action_view
/6oPT/fileadmin/b/<path:path>                 fileadmin.index_view
/6oPT/fileadmin/delete/                       fileadmin.delete
/6oPT/fileadmin/download/<path:path>          fileadmin.download
/6oPT/fileadmin/edit/                         fileadmin.edit
/6oPT/fileadmin/mkdir/                        fileadmin.mkdir
/6oPT/fileadmin/mkdir/<path:path>             fileadmin.mkdir
/6oPT/fileadmin/old_b/<path:path>             fileadmin.index
/6oPT/fileadmin/old_index                     fileadmin.index
/6oPT/fileadmin/rename/                       fileadmin.rename
/6oPT/fileadmin/upload/                       fileadmin.upload
/6oPT/fileadmin/upload/<path:path>            fileadmin.upload
/6oPT/post/                                   post.index_view
/6oPT/post/action/                            post.action_view
/6oPT/post/ajax/lookup/                       post.ajax_lookup
/6oPT/post/ajax/update/                       post.ajax_update
/6oPT/post/delete/                            post.delete_view
/6oPT/post/details/                           post.details_view
/6oPT/post/edit/                              post.edit_view
/6oPT/post/export/<export_type>/              post.export
/6oPT/post/new/                               post.create_view
/6oPT/static/<path:filename>                  admin.static
/6oPT/user/                                   user.index_view
/6oPT/user/action/                            user.action_view
/6oPT/user/ajax/lookup/                       user.ajax_lookup
/6oPT/user/ajax/update/                       user.ajax_update
/6oPT/user/delete/                            user.delete_view
/6oPT/user/details/                           user.details_view
/6oPT/user/edit/                              user.edit_view
/6oPT/user/export/<export_type>/              user.export
/6oPT/user/new/                               user.create_view
/_debug_toolbar/static/<path:filename>        _debug_toolbar.static
/_debug_toolbar/views/sqlalchemy/sql_explain  debugtoolbar.sql_select
/_debug_toolbar/views/sqlalchemy/sql_select   debugtoolbar.sql_select
/_debug_toolbar/views/template/<key>          debugtoolbar.template_editor
/_debug_toolbar/views/template/<key>          debugtoolbar.template_preview
/_debug_toolbar/views/template/<key>/save     debugtoolbar.save_template
/admin/                                       Admin.index
/admin/admin/add                              Admin.admin_add
/admin/admin/list                             Admin.admin_list
/admin/adminlog/list                          Admin.adminlog_list
/admin/comment/list                           Admin.comment_list
/admin/delete/<string:filename>               Admin.delete
/admin/delete_admin/<int:id>                  Admin.delete_admin
/admin/delete_adminlog/<int:id>               Admin.delete_adminlog
/admin/delete_comment/<int:id>                Admin.delete_comment
/admin/delete_oplog/<int:id>                  Admin.delete_oplog
/admin/delete_post/<int:id>                   Admin.delete_post
/admin/delete_role/<int:id>                   Admin.delete_role
/admin/delete_user/<int:id>                   Admin.delete_user
/admin/file/<string:filename>                 Admin.get_file
/admin/file/list                              Admin.file_list
/admin/login                                  Admin.login
/admin/logout                                 Admin.logout
/admin/oplog/list                             Admin.oplog_list
/admin/post/list                              Admin.post_list
/admin/pwd                                    Admin.pwd
/admin/role/add                               Admin.role_add
/admin/role/list                              Admin.role_list
/admin/thumb_file/<string:filename>           Admin.get_thumb_file
/admin/user/list                              Admin.user_list
/all                                          main.show_all
/auth/change-password                         auth.change_password
/auth/login                                   auth.login
/auth/logout                                  auth.logout
/auth/register                                auth.register
/avatar/<filename>                            main.get_file
/comment                                      main.comments
/delete_comment/<int:id>                      main.delete_comment
/delete_post/<int:id>                         main.delete_post
/edit-profile                                 main.edit_profile
/edit/<int:id>                                main.edit
/post/<int:id>                                main.post
/searchcomment                                main.searchcomment
/searchpost                                   main.searchpost
/static/<path:filename>                       static
/static/bootstrap/<path:filename>             bootstrap.static
/upload_file                                  main.upload_file
/user/<username>                              main.user
```

# 数据库迁移,命令
在迁移中sqlite不支持删除数据库字段
```
python manage.py db stamp 版本号 强制修改当前版本
python manage.py db init 创建migrate文件夹 注意这时候数据库是里面的version文件夹是空de
python manage.py db migrate -m "message" 根据模型设置生成迁移文件
python manage.py db history 查看migrate历史
python manage.py db upgrade 版本名 不是"message",写版本号的前缀也行
python manage.py db downgrade
python manage.py db current 查python manager.py看当前版本
```

# 说明

有部分Bug和未实现功能,比如flask-admin插件文件管理功能,等等.

想修改的小伙伴可以Pull requests