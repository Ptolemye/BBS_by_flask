from app import app
from flask import session,render_template
from config import database
@app.context_processor
def login_status():
    # 从session中获取email
    email = session.get('email')
    type=session.get('type')
    # 如果有email信息，则证明已经登录了
    if email:
            cur = database.cursor()
            sql = "select user_name from user where email = '%s'" % email
            database.ping(reconnect=True)
            cur.execute(sql)
            result = cur.fetchone()
            if result:
                return {'email':email,'username':result[0] ,'type':type}
    # 如果email信息不存在，则未登录，返回空
    return {}