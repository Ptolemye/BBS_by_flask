from app import app
from flask import render_template,request,session,flash,redirect,url_for
from config import database
import time
@app.route('/register/',methods=['GET','POST'])
def register():
    if request.method=='GET':
        return render_template('register.html')
    if request.method=='POST':
        email=request.form.get('user_email')#获取注册邮箱
        username=request.form.get('user_name')#获取昵称
        password=request.form.get('password')#获取第一次密码
        confirm_password=request.form.get('confirm_password')#获取第二次密码
        register_time = time.strftime('%Y-%m-%d %H:%M:%S')
        if not all([email,password,username,confirm_password]):
            flash('信息填写不全')
            return render_template('register.html')
        elif password!=confirm_password:
            flash('两次密码输入不一致')
            return render_template('register.html')
        cur=database.cursor()
        sql="select * from user where email='%s'"%email
        database.ping(reconnect=True)
        cur.execute(sql)
        result=cur.fetchone();
        #如果表单提交的邮箱已在数据库中
        if result is not None:
            flash('该邮箱已被注册')
            return render_template('register.html')
        else:
            sql="insert into user (email,user_name,password,register_time)" \
                "values('%s','%s','%s','%s')"%(email,username,password,register_time)
            database.ping(reconnect=True)
            cur.execute(sql)
            sql="insert into user_file(email)values ('%s')"%email
            cur.execute(sql)
            database.commit()# 持久化
            cur.close()
            return redirect(url_for('index'))


