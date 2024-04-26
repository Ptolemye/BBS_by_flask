from app import app
from flask import render_template,request,session,flash,redirect,url_for
from config import database
@app.route('/',methods=['POST','GET'])
def index():
    cur=database.cursor()
    database.ping(reconnect=True)
    user_email = session.get('email')
    # dict_result将结果转化成字典列表
    if user_email:
        sql = "select user_name,image_path from user natural join user_file where email='%s'" % user_email
        cur.execute(sql)
        result=cur.fetchone()
        #参数email
        email = {
            "user_id": user_email,
            "user_name": result[0],
            "image_path": result[1],
        }
        #参数post_brief_data
        post_brief_data = []
        if request.method=='GET':
            sql = "select post_id, email, post_time,post_title, summary,likes from post"
            cur.execute(sql)
            result = cur.fetchall()
            for i in result:
                sql = "select user_name, image_path from user natural join user_file where email='%s'" % i[1]
                cur.execute(sql)
                result1 = cur.fetchone()
                owner = {
                    'user_id': i[1],
                    'user_name': result1[0],
                    'image_path': result1[1]
                }
                post_brief = {
                    'post_id': i[0],
                    'owner': owner,
                    'time': i[2],
                    'title': i[3],
                    'summary': i[4],
                    'like_count': i[5]
                }
                post_brief_data.append(post_brief)
        if request.method=='POST':
            #获取搜索关键词
            search_term = '%'+request.form['search']+'%'
            sql="SELECT post_id, email, post_time,post_title, summary,likes " \
                "FROM post natural join user WHERE post_title LIKE %s OR summary LIKE %s OR " \
                "user_name LIKE %s OR post_id LIKE %s"
            params = (search_term, search_term, search_term, search_term)
            cur.execute(sql,params)
            result=cur.fetchall()
            for i in result:
                sql = "select user_name, image_path from user natural join user_file where email='%s'" % i[1]
                cur.execute(sql)
                result1 = cur.fetchone()
                owner = {
                    'user_id': i[1],
                    'user_name': result1[0],
                    'image_path': result1[1]
                }
                post_brief = {
                    'post_id': i[0],
                    'owner': owner,
                    'time': i[2],
                    'title': i[3],
                    'summary': i[4],
                    'like_count': i[5]
                }
                post_brief_data.append(post_brief)
        return render_template('index.html',post_brief_data = post_brief_data, email=email)
    else:
        return redirect(url_for('login'))