# MessageBoard
|- app
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
		favicon.gif
		styles.css
	|- templates
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
	|- models.py 数据库模型	
|- config.py 配置文件
|- manage.py run文件

后端考核任务

《吐槽》

根据狗书假期修改版

增加头像自定义,文件上传部分可拓展

增加一问一答形式回复功能,游客功能以及游客评论不能发布吐槽