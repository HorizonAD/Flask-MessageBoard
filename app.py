from flask import Flask,render_template,request,json,redirect,session,flash
from werkzeug.security import generate_password_hash,check_password_hash
from flask.ext.mysql import MySQL
import time


def create_app():
  app = Flask(__name__)
  return app

app = create_app()

mysql = MySQL()
app.secret_key = 'why would I tell you my secret key?'



app.config['MYSQL_DATABASE_USER'] = 'Your_Database_Username'
app.config['MYSQL_DATABASE_PASSWORD'] = 'Your_Database_Password'
app.config['MYSQL_DATABASE_DB'] = 'Your_Database'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)


@app.route('/')
def main():
    return render_template('index.html')


@app.route('/showSignUp')
def showSignUp():
    return render_template('signup.html')


@app.route('/showSignin')
def showSignin():
    if session.get('user'):
        return render_template('userHome.html')
    else:
        return render_template('signin.html')


@app.route('/userHome')
def userHome():
    if session.get('user'):
        return render_template('userHome.html')
    else:
        return render_template('error.html', error='访问未授权')


@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/')


@app.route('/validateLogin', methods=['POST'])
def validateLogin():
    try:
        _username = request.form['inputName']
        _password = request.form['inputPassword']
        con = mysql.connect()
        cursor = con.cursor()
        sql="select user_password from tbl_user where user_name='%s'"%_username
        cursor.execute(sql)
        data = cursor.fetchall()
        if len(data)>0:
            if check_password_hash(data[0][0],_password):
                session['user'] = _username
                return redirect('/userHome')
            else:
                return render_template('error.html', error='密码错误')
        else:
            return render_template('error.html', error='用户名不存在')
    except Exception as e:
        return render_template('error.html', error=str(e))


@app.route('/signUp', methods=['POST', 'GET'])
def signUp():
    try:
        _name = request.form['inputName']
        _password = request.form['inputPassword']
        if _name and _password:
            conn = mysql.connect()
            cursor = conn.cursor()
            checksql = "select exists (select 1 from tbl_user where user_name ='%s')"%_name
            cursor.execute(checksql)
            checkdata = cursor.fetchall()
            if checkdata[0][0]:
                return json.dumps({'result':'用户名已存在!'})
            else:
                _hashed_password = generate_password_hash(_password)
                sql = "insert into tbl_user(user_name,user_password) VALUES ('%s','%s')" % (_name, _hashed_password)
                cursor.execute(sql)
                data = cursor.fetchall()
                if len(data) is 0:
                    conn.commit()
                    return json.dumps({'result':'注册成功!'})
                else:
                    return json.dumps({'error': str(data[0])})
        else:
            return json.dumps({'result': '字段不能为空!'})

    except Exception as e:
        return json.dumps({'error': str(e)})

@app.route('/showAddWords')
def showAddWords():
    return render_template('addwords.html')

@app.route('/addWords',methods=['POST'])
def addWords():
    try:
        if session.get('user'):
            _description = request.form['inputDescription']
            _user = session.get('user')
            atime=time.strftime('%Y-%m-%d %H:%M:%S')
            conn = mysql.connect()
            cursor = conn.cursor()
            sql = "insert into tbl_words(words_description,words_user_id,words_date) VALUES ('%s','%s','%s')" % ( _description,_user,atime)
            cursor.execute(sql)
            data = cursor.fetchall()
            if len(data) is 0:
                conn.commit()
                return redirect('/userHome')
            else:
                return render_template('error.html', error='错误!')
        else:
            return render_template('error.html', error='访问未授权')
    except Exception as e:
        return render_template('error.html', error=str(e))
    finally:
        cursor.close()
        conn.close()

@app.route('/getAllWords')
def getAllWords():
    try:
        if session.get('user'):
            conn = mysql.connect()
            cursor = conn.cursor()
            sql="select * from tbl_words"
            cursor.execute(sql)
            result = cursor.fetchall()
            words_dict = []
            for word in result:
                word_dict = {
                    'Id': word[2],
                    'Description': word[1],
                    'Time':word[3]
                }
                words_dict.append(word_dict)
            return json.dumps(words_dict)
        else:
            return render_template('error.html', error='访问未授权')
    except Exception as e:
        return render_template('error.html', error=str(e))

@app.route('/404', methods = ['GET', 'POST'])
def errorhtm():
    return render_template("404.html"),404

if __name__=="__main__":
    app.debug = True
    app.run()