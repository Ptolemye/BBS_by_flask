from app import app
from flask import render_template,request,session,flash,redirect,url_for
from config import database

def post_brief_data_prepare(result):
    cur = database.cursor()
    post_brief_data = []
    for i in result:
        # 获取帖主信息
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
    return post_brief_data

email = {
        "user_id": "admin",
        "user_name": "管理员",
        "image_path": "images/admin.png",
    }
@app.route('/admin/',methods=['GET','POST'])
def admin_home():
    if request.method=='GET':
        type=session.get('type')
        if type is None:
            return redirect(url_for('login'))
        if type==0:
            return redirect(url_for('login'))
        if type==1:
            return render_template('/admin/base.html',email=email)
@app.route('/admin/<name>/', methods=['GET','POST'])
def admin(name):
    cur=database.cursor()
    if request.method == 'GET':
        pass_data = True
        data = []
        query = request.values.get('query')
        cur=database.cursor()
        database.ping(reconnect=True)
        if name == 'posts' and pass_data:
            #获取帖子信息
            sql = "select post_id, email, post_time,post_title, summary,likes from post"
            cur.execute(sql)
            result = cur.fetchall()
            # post_brief_data = []
            # for i in result:
            #     #获取帖主信息
            #     sql = "select user_name, image_path from user natural join user_file where email='%s'" % i[1]
            #     cur.execute(sql)
            #     result1 = cur.fetchone()
            #     owner = {
            #         'user_id': i[1],
            #         'user_name': result1[0],
            #         'image_path': result1[1]
            #     }
            #     post_brief = {
            #         'post_id': i[0],
            #         'owner': owner,
            #         'time': i[2],
            #         'title': i[3],
            #         'summary': i[4],
            #         'like_count': i[5]
            #     }
            #     post_brief_data.append(post_brief)
            data = post_brief_data_prepare(result)
        elif name == 'users' and pass_data:
            sql="select email,user_name,image_path,ban,register_time,profile from user natural join user_file WHERE email != 'admin'"
            cur.execute(sql)
            result=cur.fetchall()
            columns=['user_id','user_name','image_path','blocked','user_register_time','content']
            dict_result = [dict(zip(columns, row)) for row in result]
            data = dict_result
        elif name == 'reports' and pass_data:
            sql = "select report_id,reporter_email,post_id,post_title,reason,report_time from report natural join post"
            cur.execute(sql)
            result = cur.fetchall()
            columns = ['report_id','reporter_id', 'post_id','post_title', 'content','time']
            dict_result = [dict(zip(columns, row)) for row in result]
            data = dict_result
        return render_template(f'/admin/{name}.html',
                            front_data = data,email=email)
    if request.method=='POST':
        if name=='posts':
            if 'delete_post' in request.form:
                # 获取需要删除的帖子id
                post_id = request.form.get('delete_post')
                sql = "delete from post where post_id='%s'" % post_id
                cur.execute(sql)
                # 删除帖子的评论
                sql = "delete from comment where post_id='%s'" % post_id
                cur.execute(sql)
                database.commit()  # 持久化
                cur.close()
                return redirect(url_for('admin', name='posts'))
            if 'query' in request.form:
                search_term = '%' + request.form['query'] + '%'
                sql = "SELECT post_id, email, post_time,post_title, summary,likes " \
                      "FROM post natural join user WHERE post_title LIKE %s OR summary LIKE %s OR " \
                      "user_name LIKE %s"
                params = (search_term, search_term, search_term)
                cur.execute(sql, params)
                result = cur.fetchall()
                data = post_brief_data_prepare(result)
                return render_template(f'/admin/{name}.html',
                                       front_data=data, email=email)
        if name=='users':
            if 'delete' in request.form:
                user_id=request.form.get('delete')
                #删除账户
                sql = "delete from user where email='%s'"%user_id
                cur.execute(sql)
                #删除账户简介
                sql = "delete from user_file where email='%s'" % user_id
                cur.execute(sql)
                #删除账户帖子
                sql = "delete from post where email='%s'" % user_id
                cur.execute(sql)
                #删除用户评论
                sql = "delete from comment where user_email='%s'" % user_id
                cur.execute(sql)
                database.commit()
                cur.close()
                return redirect(url_for('admin',name='users'))
            if 'block' in request.form:
                user_id=request.form.get('block')
                sql = "UPDATE user SET ban = '1' WHERE email = '%s'" % user_id
                cur.execute(sql)
                database.commit()
                cur.close()
                return redirect(url_for('admin', name='users'))
            if 'unblock' in request.form:
                user_id = request.form.get('unblock')
                sql = "UPDATE user SET ban = '0' WHERE email = '%s'" % user_id
                cur.execute(sql)
                database.commit()
                cur.close()
                return redirect(url_for('admin', name='users'))
            if 'query' in request.form:
                search_term = '%' + request.form['query'] + '%'
                sql = " select email,user_name,image_path,ban,register_time,profile from user natural join user_file " \
                      "WHERE user_name LIKE %s OR profile LIKE %s OR email LIKE %s"
                params = (search_term, search_term,search_term)
                cur.execute(sql, params)
                result = cur.fetchall()
                columns = ['user_id', 'user_name', 'image_path', 'blocked', 'user_register_time', 'content']
                dict_result = [dict(zip(columns, row)) for row in result]
                data = dict_result
                return render_template(f'/admin/{name}.html',
                                       front_data=data, email=email)
        if name=='reports':
            if 'delete_report' in request.form:
                report_id=request.form.get('delete_report')
                sql = "delete from report where report_id='%s'" % report_id
                cur.execute(sql)
                database.commit()  # 持久化
                cur.close()
                return redirect(url_for('admin',name='reports'))
            if 'query' in request.form:
                search_term = '%' + request.form['query'] + '%'
                sql = "select report_id,reporter_email,post_id,post_title,reason,report_time " \
                      "FROM report natural join post WHERE report_id LIKE %s OR post_id LIKE %s OR " \
                      "post_title LIKE %s OR reason LIKE %s"
                params = (search_term, search_term, search_term,search_term)
                cur.execute(sql, params)
                result = cur.fetchall()
                columns = ['report_id', 'reporter_id', 'post_id', 'post_title', 'content', 'time']
                dict_result = [dict(zip(columns, row)) for row in result]
                data = dict_result
                return render_template(f'/admin/{name}.html',
                                       front_data=data, email=email)

@app.route('/admin/comments/<post_id>/', methods=['GET', 'POST'])
def admin_comment(post_id):
    cur=database.cursor()
    if request.method == 'GET':
        database.ping(reconnect=True)
        # 寻找post_id对应的评论表
        sql="select comment_id,user_email,comment_content,comment_time from comment where post_id='%s'"%post_id
        cur.execute(sql)
        result=cur.fetchall()
        comments=[]
        for i in result:
            sql = "select email,user_name,image_path from user natural join user_file WHERE email = '%s'"%i[1]
            cur.execute(sql)
            result1=cur.fetchone()
            critic={
                "user_id" :result1[0] ,
                "user_name": result1[1] ,
                "image_path": result1[2]
            }
            comment={
                "comments_id": i[0],
                "post_id": post_id,
                "critic": critic,
                "time":i[3] ,
                "content": i[2]
            }
            comments.append(comment)
        test_data = comments
        return render_template(f"/admin/comments.html",
                           post_id = post_id,
                           front_data = test_data,
                           email = email)
    elif request.method == 'POST':
        if 'query' in request.form:
            search_term = '%' + request.form['query'] + '%'
            sql = "select comment_id,user_email,comment_content,comment_time " \
                  "FROM  comment  WHERE comment_id LIKE %s OR user_email LIKE %s OR " \
                  "comment_content LIKE %s AND post_id=%s"
            params = (search_term, search_term, search_term,post_id)
            cur.execute(sql, params)
            result = cur.fetchall()
            comments = []
            for i in result:
                sql = "select email,user_name,image_path from user natural join user_file WHERE email = '%s'" % i[1]
                cur.execute(sql)
                result1 = cur.fetchone()
                critic = {
                    "user_id": result1[0],
                    "user_name": result1[1],
                    "image_path": result1[2]
                }
                comment = {
                    "comments_id": i[0],
                    "post_id": post_id,
                    "critic": critic,
                    "time": i[3],
                    "content": i[2]
                }
                comments.append(comment)
            test_data = comments
            return render_template(f"/admin/comments.html",
                                   post_id=post_id,
                                   front_data=test_data,
                                   email=email)
        if 'delete_comment' in request.form:
            comment_id=request.form.get('delete_comment')
            sql="delete from comment where comment_id='%s'"%comment_id
            cur.execute(sql)
            database.commit()
            cur.close()
            return redirect(url_for('admin_comment',post_id=post_id))