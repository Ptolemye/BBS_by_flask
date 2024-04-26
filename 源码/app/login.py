from app import app
from flask import render_template,request,session,flash,redirect,url_for
from config import database
@app.route('/login/',methods=['GET','POST'])
def login():
    if request.method=='GET':
        return render_template('login.html')
    if request.method=='POST':
        identifier = request.form.get('identifier')
        if identifier == 'user_login':
        #处理管理员登录按钮的逻辑
            email=request.form.get('user_email')#获取参数email
            password=request.form.get('password')#获取参数password
            if not all([email,password]):
                flash('填写信息不全')
                return render_template('login.html')
            cur=database.cursor()
            database.ping(reconnect=True)
            sql="select password,ban from user where email='%s'"%email
            cur.execute(sql)
            result=cur.fetchone()
            if result is None:
                flash('该用户未注册')
                return render_template('login.html')
            #若账号正在封禁中，则无法登录
            if result[1]==1:
                flash('你的账号已被封禁')
                return render_template('login.html')
            if result[0]==password:
                session['email']=email##用session记录当前登录的用户
                session['type']=0#普通用户登录，type字段记录为0
                return redirect(url_for('index'))
            else:
                flash('密码不正确')
                return render_template('login.html')
        if identifier == 'admin_login':
            email = request.form.get('user_email')  # 获取参数email
            password = request.form.get('password')  # 获取参数password
            cur = database.cursor()
            database.ping(reconnect=True)
            sql = "select password from admin where email='%s'" % email
            cur.execute(sql)
            result = cur.fetchone()
            if result is None:
                flash('不存在此管理员')  # 弹出flash消息
                return render_template('login.html')
            if result[0] == password:
                session['email'] = 'admin'  ##用session记录当前登录的用户 12.4 13:06
                session['type'] = 1  # 管理员登录，type字段记录为1
                return redirect(url_for('admin_home'))
            else:
                flash('密码不正确')
                return render_template('login.html')