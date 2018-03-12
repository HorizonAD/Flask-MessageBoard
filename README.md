# 留言板
![Packagist](https://img.shields.io/packagist/l/doctrine/orm.svg)  ![Python](https://img.shields.io/badge/python-%203.4,%203.5,%203.6-blue.svg)  ![Bootstrap](https://img.shields.io/badge/Bootstrap-3.0-yellowgreen.svg)  ![Docker Automated build](https://img.shields.io/docker/automated/jrottenberg/ffmpeg.svg)


在线Demo：(不久可能会失效)[吐点槽吧](http://liuyan.flywinky.top/)

# 本地预览

## Docker启动

- 修改docker-compose.yml中数据文件地址成在你服务器的绝对路径
(使用sqlite,这样可以做好数据保存)

- 输入下面指令一键启动(需提前安装docker-compose)
```
docker-compose up -d
```
浏览器打开 http://127.0.0.1:5000 即可

## 源码安装

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

- 结合bootstrap3,自定义后台 [https://adminlte.io/premium](https://adminlte.io/premium)
  Bootstrap3部分静态文件在部署时可以删去

- 文件浏览前端样式 [https://github.com/blueimp/jQuery-File-Upload](https://github.com/blueimp/jQuery-File-Upload)

![演示](http://on2mh1s1f.bkt.clouddn.com/QQ%E6%88%AA%E5%9B%BE20170906153214.png?imageView2/0/q/75|watermark/2/text/5YWr5LiA/font/5b6u6L2v6ZuF6buR/fontsize/600/fill/I0U5MjQyNA==/dissolve/100/gravity/SouthEast/dx/10/dy/10|imageslim)

# 所有url
可以使用python manage.py showurls生成

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

我设置了用户为<strong>八一</strong>才能进到后台链接的

![逻辑](http://on2mh1s1f.bkt.clouddn.com/QQ%E6%88%AA%E5%9B%BE20170924111631.jpg)

有部分Bug和未实现功能,比如flask-admin插件文件管理功能,等等.

想修改的小伙伴可以Pull requests