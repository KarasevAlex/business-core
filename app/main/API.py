from . import main
from ..database import Partner, News, Team
from .. import db
from flask import Flask, render_template, request
from flask import Flask, request, redirect, url_for
from werkzeug.utils import secure_filename
import uuid, os
from flask_login import current_user


ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif', 'JPG'])

def allowed_filename(filename):
    return '.' in filename and filename.rsplit('.',1)[1] in ALLOWED_EXTENSIONS

def upload(file):
    if file and allowed_filename(file.filename):
        filename = secure_filename(file.filename)
        mypath = main.root_path[:-4] + '/static/img/picturs'
        if os.path.exists(mypath) != True:
            os.mkdir(mypath)
        _filename = str(uuid.uuid4().hex) + '.' + filename.rsplit('.', 1)[1]
        try:
            file.save(os.path.join(mypath, _filename))
            return _filename
        except:
            return

@main.route('/partner/add', methods=['POST'])
def partners_add():
    filename = upload(request.files['file'])
    if filename is not None:
        partner = Partner(picture=filename, name=request.form['description'])
        db.session.add(partner)
        return redirect('/partners')

@main.route('/partner/remove/<int:id>', methods=['GET'])
def partners_remove(id):
    obj = Partner.query.filter_by(id=id).first()
    mypath = main.root_path[:-4] + '/static/img/picturs/' + obj.picture
    os.remove(mypath)
    db.session.delete(obj)
    return redirect('/partners')

@main.route('/member/add', methods=['POST'])
def member_add():
    filename = upload(request.files['file'])
    if filename is not None:
        member = Team(picture=filename, name=request.form['name'], discription=request.form['description'])
        db.session.add(member)
        return redirect('/team')

@main.route('/member/remove/<int:id>', methods=['GET'])
def member_remove(id):
    obj = Team.query.filter_by(id=id).first()
    mypath = main.root_path[:-4] + '/static/img/picturs/' + obj.picture
    os.remove(mypath)
    db.session.delete(obj)
    return redirect('/team')

@main.route('/news/add', methods=['POST'])
def add_news():
    try:
        temp = News(title=request.form['title'],
            text=request.form['text'],
            timestamp=request.form['date'],
            author_id=current_user.id)
        db.session.add(temp)
        db.session.commit()
        return redirect('/news')
    except:
        pass

@main.route('/news/remove/<int:id>', methods=['POST'])
def remove_news(id):
    News.query.filter_by(id=id).delete()
    return redirect('/news')