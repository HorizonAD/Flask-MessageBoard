# MessageBoard
演示：(不久可能会失效)[吐点槽吧](http://cumt.studio/)		
		
# 项目结构
```
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
	|- __init__.py 初始化app文件
	|- email.py email配置以及异步实现
	|- exceptions.py 异常处理	
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