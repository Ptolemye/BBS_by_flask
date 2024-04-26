from app import app, id_creater
from config import database as db
from flask import render_template, request, redirect, url_for, session
import time


@app.route('/post/<id>/', methods=['GET', 'POST'])
def post(id):
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

        # 获取帖子的发帖人email(id)
        sql = "select email from post where post_id = '%s'" % id
        db.ping(reconnect=True)
        cur.execute(sql)
        author_email = cur.fetchone()[0]

        # 通过发帖子人的email(id)获取其image_path
        sql = "select image_path from user_file where email = '%s'" % author_email
        db.ping(reconnect=True)
        cur.execute(sql)
        author_image_path = cur.fetchone()[0]

        # 通过发帖人email(id)获取其name
        sql = "select user_name from user where email = '%s'" % author_email
        db.ping(reconnect=True)
        cur.execute(sql)
        author_name = cur.fetchone()[0]

        author_brief_data = {
            "user_id": author_email,
            "user_name": author_name,
            "image_path": author_image_path,
        }

        # 帖子详情
        post_id = id
        post_owner = author_brief_data

        sql = "select post_time, post_title, content, likes from post where post_id = '%s'" % id
        db.ping(reconnect=True)
        cur.execute(sql)
        result = cur.fetchone()
        post_time = result[0]
        post_title = result[1]
        post_content = result[2]
        post_likes = result[3]
        post_details = {
            "post_id": post_id,
            "owner": post_owner,
            "time": post_time,
            "title": post_title,
            "content": post_content,
            "like_count": post_likes
        }

        sql = ("select comment_id, post_id, user_email, comment_time,comment_content "
               "from comment where post_id = '%s' "
               "order by comment_time desc ") % id
        db.ping(reconnect=True)
        cur.execute(sql)
        result = cur.fetchall()
        comments = []
        for item in result:
            commentator_id = item[2]
            sql = "select user_name from user where email = '%s'" % commentator_id
            db.ping(reconnect=True)
            cur.execute(sql)
            commentator_name = cur.fetchone()[0]
            sql = "select image_path from user_file where email = '%s'" % commentator_id
            db.ping(reconnect=True)
            cur.execute(sql)
            commentator_image_path = cur.fetchone()[0]
            commentator_brief_data = {
                "user_id": commentator_id,
                "user_name": commentator_name,
                "image_path": commentator_image_path,
            }
            comment = {
                "comments_id": item[0],
                "post_id": item[1],
                "critic": commentator_brief_data,
                "time": item[3],
                "content": item[4]
            }
            comments.append(comment)
        cur.close()
        print(111)
        print(post, comments, email)
        return render_template('post.html', post_data=post_details, comments=comments, email=email)

    elif request.method == 'POST':
        user_email = session.get('email')
        if user_email is None:
            return redirect(url_for('login'))

        identifier = request.form.get('identifier')
        if identifier == 'like':
            cur = db.cursor()
            sql = "update post set likes = likes+1 where post_id = '%s'" % id
            db.ping(reconnect=True)
            cur.execute(sql)
            db.commit()
            cur.close()
            return redirect(url_for('post', id=id))
        elif identifier == 'post_comment':
            commentator_email = session.get('email')
            comment_content = request.form.get('comment')
            comment_time = time.strftime('%Y-%m-%d %H:%M:%S')
            comment_id = 'c' + id_creater.id_creater()
            cur = db.cursor()
            sql = "select * from comment where comment_id = '%s'" % comment_id
            db.ping(reconnect=True)
            cur.execute(sql)
            result = cur.fetchone()
            while result is not None:
                comment_id = 'c' + id_creater.id_creater()
                cur = db.cursor()
                sql = "select * from comment where comment_id = '%s'" % comment_id
                db.ping(reconnect=True)
                cur.execute(sql)
                result = cur.fetchone()

            sql = ("insert into comment (comment_id, user_email, post_id, comment_content, comment_time) values "
                   "('%s','%s','%s','%s','%s')") % \
                  (comment_id, commentator_email, id, comment_content, comment_time)

            db.ping(reconnect=True)
            cur.execute(sql)
            db.commit()
            cur.close()
            return redirect(url_for('post', id=id))
        elif identifier == 'report':
            reporter_email = session.get('email')
            report_time = time.strftime('%Y-%m-%d %H:%M:%S')
            report_reason = request.form.get('content')
            report_id = 'r' + id_creater.id_creater()
            cur = db.cursor()
            sql = "select * from report where report_id = '%s'" % report_id
            db.ping(reconnect=True)
            cur.execute(sql)
            result = cur.fetchone()
            while result is not None:
                report_id = 'r' + id_creater.id_creater()
                cur = db.cursor()
                sql = "select * from report where report_id = '%s'" % report_id
                db.ping(reconnect=True)
                cur.execute(sql)
                result = cur.fetchone()
            sql = ("insert into report (report_id, post_id, reporter_email, report_time, reason) VALUES ('%s','%s',"
                   "'%s','%s','%s')") % (report_id, id, reporter_email, report_time, report_reason)
            db.ping(reconnect=True)
            cur.execute(sql)
            db.commit()
            cur.close()
            return redirect(url_for('post', id=id))