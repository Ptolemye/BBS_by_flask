from app import app
from flask import render_template,request,session,flash,redirect,url_for

@app.route('/logout/')
def logout():
    session.clear()
    return redirect(url_for('index'))