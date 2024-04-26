import json
from app import app
from flask import render_template,request,redirect,url_for

user_brief_data = [
    {
        "user_id" : "202101",
        "user_name": "user01",
        "image_path": "images/user01.png",
    },
    {
        "user_id" : "202102",
        "user_name": "user02",
        "image_path": "images/user02.png",
    },
    {
        "user_id" : "202103",
        "user_name": "user03",
        "image_path": "images/user03.png",
    },
]

post_brief_data = [
    {
        "post_id": "P1024",
        "owner": user_brief_data[0],
        "time": "2021-19-1",
        "title": "这是一个测试帖子",
        "summary": "这是测试帖子的简介",
        "like_count": 123
    },
    {
        "post_id": "P1025",
        "owner": user_brief_data[0],
        "time": "2021-19-1",
        "title": "这是一个测试帖子",
        "summary": "这是测试帖子的简介",
        "like_count": 123
    },
    {
        "post_id": "P1024",
        "owner": user_brief_data[0],
        "time": "2021-19-1",
        "title": "这是一个测试帖子",
        "summary": "这是测试帖子的简介",
        "like_count": 123
    },
    {
        "post_id": "P1024",
        "owner": user_brief_data[0],
        "time": "2021-19-1",
        "title": "这是一个测试帖子",
        "summary": "这是测试帖子的简介",
        "like_count": 123
    }
]

user_data = [
    {
        "user_id" : "202101",
        "user_name": "user01",
        "image_path": "images/user01.png",
        "blocked": False,
        "user_register_time": "2121.15.4",
        "content": "这是用户user01的个人简介",
    },
    {
        "user_id" : "202102",
        "user_name": "user02",
        "image_path": "images/user02.png",
        "blocked": True,
        "user_register_time": "2121.15.4",
        "content": "这是用户user02的个人简介",
    },
    {
        "user_id" : "202103",
        "user_name": "user03",
        "image_path": "images/user03.png",
        "blocked": False,
        "user_register_time": "2121.15.4",
        "content": "这是用户user03的个人简介",
    }
]

post_data = [
    {
        "post_id": "P1024",
        "owner": user_brief_data[0],
        "time": "2021-19-21",
        "title": "求和",
        "content": "<p>hello world</p>",
        "like_count": 123
    },
    {
        "post_id": "P1025",
        "owner": user_brief_data[1],
        "time": "2021-19-21",
        "title": "求和",
        "content": "<p>it is nice to see you</p>",
        "like_count": 123
    }
]

comments = [
    {
        "comments_id": "c10244",
        "post_id": "P1024",
        "critic": user_brief_data[1],
        "time": "2023-12-3",
        "content": "这是一个测试评论"
    },
    {
        "comments_id": "c10244",
        "post_id": "P1024",
        "critic": user_brief_data[1],
        "time": "2023-12-3",
        "content": "这是一个测试评论"
    },
]

report_data = [
    {
        "reporter": "20232@qq.com", #email
        "post_id": "20121363891",
        "post_title": "XXXX",
        "reason": "xxxxxxxx",
        "time": "2021-222-2",
    },
    {
        "reporter": "20232@qq.com", #email
        "post_id": "20121363891",
        "post_title": "XXXX",
        "reason": "xxxxxxxx",
        "time": "2021-222-2",
    },
    {
        "reporter": "20232@qq.com", #email
        "post_id": "20121363891",
        "post_title": "XXXX",
        "reason": "xxxxxxxx",
        "time": "2021-222-2",
    },
    {
        "reporter": "20232@qq.com", #email
        "post_id": "20121363891",
        "post_title": "XXXX",
        "reason": "xxxxxxxx",
        "time": "2021-222-2",
    }
]

email = {
    "user_id" : "202101",
    "user_name": "user01",
    "image_path": "images/user01.png",
}

filename = "data.json"

# 前端测试用路由
@app.route('/', methods=['GET','POST'])
def index():
    test = []
    test = post_brief_data
    return render_template('index.html', post_brief_data = test, email=email)

@app.route('/login/',methods=['GET','POST'])
def login():
    if request.method=='GET':
        return render_template('login.html')
    if request.method == 'POST':
        return redirect(url_for('index'))
    
    
@app.route('/register/',methods=['GET','POST'])
def register():
    if request.method=='GET':
        return render_template('register.html')
    
@app.route('/post/<id>/',methods=['GET','POST'])
def post(id):
    if request.method=='GET':
        for post in post_data:
            if post['post_id'] == id:
                return render_template('/post.html', post_data=post, comments=comments, email=email)
        return "file not found!"
                
        

@app.route('/profile/<user_id>/<part>/')
def profile(user_id, part):
    for i in user_data:
        if i["user_id"] == user_id:
            if part == 'introduct':
                return render_template(f'/profile/{part}.html', user_data=i, email=email)
            elif part == 'posts':
                return render_template(f'/profile/{part}.html', user_posts = post_brief_data, email=email)
            elif part == 'comments':
                return render_template(f'/profile/{part}.html', user_comments = comments, email=email)
            

@app.route('/publish/',methods=['GET','POST'])
def publish():
    if request.method == 'GET':
        return render_template('/publish.html', email=email)
    elif request.method == 'POST':
        return redirect(url_for('index'))
    

@app.route('/admin/<name>/', methods=['GET','POST'])
def admin(name):
    if request.method == 'GET':
        pass_data = True
        data = []
        if name == 'posts' and pass_data:
            data = post_data
        elif name == 'users' and pass_data:
            data = user_data
        elif name == 'reports' and pass_data:
            data = report_data
        return render_template(f'/admin/{name}.html',
                            front_data = data,
                            email=email)
    elif request.method == 'POST':
        return render_template('login.html')

@app.route('/logout')
def logout():
    return render_template('/login.html')


@app.route('/upload', methods=['POST'])
def upload():
    avatar = request.files['avatar']

    return '文件上传成功'