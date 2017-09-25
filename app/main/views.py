from . import main
from .. import db
from .forms import Login as Login_form
from ..database import User
from flask import render_template, request, flash,redirect
from flask_login import login_user, logout_user, login_required


@main.route('/create_database', methods=['GET', 'POST'])
def create_database():
    try:
        db.create_all()
        return "succed"
    except:
        return "fail"

@main.route('/', methods=['POST','GET'])
def index():
    login = Login_form(request.form)
    return render_template('layout.html',
                           header=render_template('header.html'),
                           main=render_template('index.html', form=login),
                           footer=render_template('footer.html'))

@main.route('/login', methods=['POST'])
def index_():
    form = Login_form()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.login.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, remember=True)
            return redirect('/2')
        flash('Invalid login or password')
    return render_template('index.html', form=form)

@main.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')


@login_required
@main.route('/2')
def index2():
    return render_template('layout.html',
                           header=render_template('header.html'),
                           main=render_template('admin-list.html'),
                           footer=render_template('footer.html'))

@main.route('/3')
def index3():
    return render_template('layout.html',
                           header=render_template('header.html'),
                           main=render_template('admin-session.html'),
                           footer=render_template('footer.html'))

@main.route('/4')
def index4():
    return render_template('layout.html',
                           header=render_template('header.html'),
                           main=render_template('album.html'),
                           footer=render_template('footer.html'))

@main.route('/5')
def index5():
    return render_template('layout.html',
                           header=render_template('header.html'),
                           main=render_template('contacts.html'),
                           footer=render_template('footer.html'))

@login_required
@main.route('/6')
def index6():
    return render_template('layout.html',
                           header=render_template('header.html'),
                           main=render_template('gallery.html'),
                           footer=render_template('footer.html'))

@main.route('/7')
def index7():
    return render_template('layout.html',
                           header=render_template('header.html'),
                           main=render_template('news.html'),
                           footer=render_template('footer.html'))

@main.route('/8')
def index9():
    return render_template('layout.html',
                           header=render_template('header.html'),
                           main=render_template('partners.html'),
                           footer=render_template('footer.html'))

@main.route('/9')
def index10():
    return render_template('layout.html',
                           header=render_template('header.html'),
                           main=render_template('user-session.html'),
                           footer=render_template('footer.html'))

