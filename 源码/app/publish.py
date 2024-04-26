from app import app, id_creater
from flask import render_template, request, redirect, url_for, session
from config import database as db
import time


# 用户发帖
@app.route('/publish/', methods=['GET', 'POST'])
def publish():
    if request.method == 'GET':
        user_email = session.get('email')
        if user_email is None:
            return redirect(url_for('login'))
        cur = db.cursor()
        sql = "select user_name from user where email = '%s'" % user_email
        db.ping(reconnect=True)
        cur.execute(sql)
        user_name = cur.fetchone()[0]
        sql = "select image_path from user_file where email = '%s'" % user_email
        db.ping(reconnect=True)
        cur.execute(sql)
        user_image_path = cur.fetchone()[0]
        email = {
            "user_id": user_email,
            "user_name": user_name,
            "image_path": user_image_path,
        }

        return render_template('publish.html', email=email)

    elif request.method == 'POST':
        # 获取发帖用户的信息
        email = session.get('email')
        post_title = request.form.get('title')
        post_summary = request.form.get('summary')
        post_content = request.form.get('content')
        post_likes = 0
        post_time = time.strftime('%Y-%m-%d %H:%M:%S')

        post_id = 'p' + id_creater.id_creater()
        cur = db.cursor()
        sql = "select * from post where post_id = '%s'" % post_id
        db.ping(reconnect=True)
        cur.execute(sql)
        result = cur.fetchone()
        while result is not None:
            post_id = 'p' + id_creater.id_creater()
            sql = "select * from post where post_id = '%s'" % post_id
            db.ping(reconnect=True)
            cur.execute(sql)
            result = cur.fetchone()

        sql = ("insert into post (post_id, email, post_title, content, post_time, likes, summary) VALUES ('%s',"
               "'%s','%s','%s','%s','%d','%s')") % (post_id, email, post_title, post_content,
                                                    post_time, post_likes, post_summary)
        db.ping(reconnect=True)
        cur.execute(sql)
        db.commit()
        cur.close()
        return redirect(url_for('index'))