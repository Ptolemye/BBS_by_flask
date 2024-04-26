from app import app
from app.id_creater import id_creater
from config import database
from flask import render_template, request, session,  redirect, url_for
import  os
@app.route('/profile/<user_id>/<part>/',methods=['GET','POST'])
def profile(user_id, part):
    cur = database.cursor()
    database.ping(reconnect=True)
    # 获取登录用户个人信息
    user_email = session.get('email')
    sql = "select email,user_name,image_path from user natural join user_file where email='%s'" % user_email
    cur.execute(sql)
    result = cur.fetchone()
    columns = ['user_id', 'user_name', 'image_path']  # 获取email
    email = dict(zip(columns, result))
    database.ping(reconnect=True)
    # 获取被访问用户个人信息
    sql = "select email,user_name,image_path from user natural join user_file where email='%s'" % user_id
    cur.execute(sql)
    result = cur.fetchone()
    columns = ['user_id', 'user_name', 'image_path']  # 获取requst_email
    request_email = dict(zip(columns, result))
    database.ping(reconnect=True)
    # 获取被访问用户的个人信息
    sql = "select email,user_name,image_path,ban,register_time,profile " \
          "from user natural join user_file where email='%s'" % user_id
    cur.execute(sql)
    result = cur.fetchone()
    columns = ['user_id', 'user_name', 'image_path', 'blocked', 'user_register_time', 'content']
    user_data = dict(zip(columns, result))
    if request.method=='GET':
        if part == 'introduct':
            return render_template(f'/profile/{part}.html', user_data=user_data, email=email)
        elif part == 'posts':
            database.ping(reconnect=True)
            #获取该用户的帖子
            sql="select post_id, post_time,post_title, summary,likes " \
                "from post where email='%s'"%user_id
            cur.execute(sql)
            result=cur.fetchall()
            post_brief_data=[]
            for i in result:
                post_brief={
                    'post_id':i[0],
                    'owner':request_email,
                    'time':i[1],
                    'title':i[2],
                    'summary':i[3],
                    'like_count':i[4]
                }
                post_brief_data.append(post_brief)
            return render_template(f'/profile/{part}.html', user_posts=post_brief_data, user_data=user_data,email=email)
        elif part == 'comments':
            database.ping(reconnect=True)
            #获取该用户的评论
            sql="select comment_id,post_id,comment_content,comment_time " \
                "from comment where user_email='%s'"%user_id
            cur.execute(sql)
            user_comments=cur.fetchall()
            comments=[]
            for i in user_comments:
                comment={
                    "comments_id": i[0],
                    "post_id": i[1],
                    "critic": request_email,
                    "time": i[3],
                    "content": i[2]
                }
                comments.append(comment)
            return render_template(f'/profile/{part}.html', user_comments=comments, user_data=user_data,email=email)
    if request.method=='POST':
        if part == 'introduct':
            identifier = request.form.get('identifier')
            if identifier == 'upload_image':
                avatar_file = request.files['avatar']
                #随机生成图像id
                filename ='u'+id_creater()+'.png'
                image_path='images/'+filename
                sql = "select * from user_file where image_path='%s'" % image_path
                cur.execute(sql)
                result=cur.fetchone()
                #持续生成id直到id在数据库中不存在
                while result is not None:
                    filename = id_creater() + '.png'
                    image_path = 'images/u' + filename
                    sql = "select * from user_file where image_path='%s'" % image_path
                    cur.execute(sql)
                    result = cur.fetchone()
                # 构建保存文件的路径
                uploads_dir = os.path.join(app.root_path, 'static', 'images')
                os.makedirs(uploads_dir, exist_ok=True)
                file_path = os.path.join(uploads_dir, filename)
                # 保存文件到本地
                avatar_file.save(file_path)
                #保存路径
                sql="UPDATE user_file SET image_path = '%s' WHERE email = '%s'"%(image_path,user_id)
                cur.execute(sql)
                database.commit()
                cur.close()
            if identifier=='modify_user_data':
                user_name = request.form['user_name']
                user_profile = request.form['user_profile']
                sql = "UPDATE user_file SET profile = '%s' WHERE email = '%s'" % (user_profile, user_id)
                cur.execute(sql)
                sql="UPDATE user SET user_name = '%s' WHERE email = '%s'"% (user_name, user_id)
                cur.execute(sql)
                database.commit()
                cur.close()
            return redirect(url_for('profile',user_id=user_id, part='introduct'))
        elif part == 'posts':
            # 获取需要删除的帖子id
            post_id = request.form.get('delete_post')
            sql="delete from post where post_id='%s'"%post_id
            cur.execute(sql)
            #删除帖子的评论
            sql="delete from comment where post_id='%s'"%post_id
            cur.execute(sql)
            database.commit()  # 持久化
            cur.close()
            return redirect(url_for('profile',user_id=user_id, part='posts'))
        elif part == 'comments':
            #获取需要删除的评论id
            comment_id = request.form.get('delete_comment')
            sql="delete from comment where comment_id='%s'"%comment_id
            cur.execute(sql)
            database.commit()  # 持久化
            cur.close()
            return redirect(url_for('profile',user_id=user_id, part='comments'))

@app.route('/upload', methods=['POST'])
def upload():
    avatar = request.files['avatar']
    return '文件上传成功'