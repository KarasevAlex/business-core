import flask_excel as excel
import xlsxwriter
from . import main
from .. import db
from .chart import Chart
from .modeling import Modeling
from .decorators import admin_required, gamer_required
from .forms import Login as Login_form, News as News_form
from ..database import User, Games, Period, Solutions, News
from flask import render_template, request, flash,redirect, send_from_directory
from flask_login import login_user, logout_user, login_required, current_user


@main.route('/create_database', methods=['GET', 'POST'])
def create_database():
    try:
        db.create_all()
        db.session.add(User(username='Admin', password='Admin', role=1))
        return "succed"
    except Exception as e:
        return "fail"

@main.route('/', methods=['POST','GET'])
def index():
    login = Login_form(request.form)
    return render_template('layout.html',
                           header=render_template('header.html', form=login),
                           main=render_template('index.html'),
                           footer=render_template('footer.html'))

@main.route('/login', methods=['POST'])
def index_():
    form = Login_form()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.login.data).first()
        if user is not None:
            if user.verify_password(form.password.data):
                if user.role == 3:
                    login_user(user, remember=True)
                    return redirect('/play')
                else:
                    login_user(user, remember=True)
                    return redirect('/game')
        flash('Invalid login or password')
    return render_template('index.html', form=form)

@main.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')


@main.route('/game', methods=['POST', 'GET'])
@login_required
@admin_required
def index2():
    if request.method == "POST":
        Games.create(request.form)
    games = Games.query.all()
    return render_template('layout.html',
                           header=render_template('header.html', form=Login_form()),
                           main=render_template('admin-list.html', games=games),
                           footer=render_template('footer.html'))


@main.route('/game/<int:id>')
@login_required
def session_admin(id):
    games = Games.query.filter_by(id=id)
    users = User.query.filter_by(game_id=id).all()
    periods = Period.query.filter_by(game_id=id)
    # current_period = Period.getActivePeriod(id)
    # if current_period is not None:
    #     previous_solution = None
    #     if current_period.period_number != 1:
    #         previous_solution = Solutions.getPreviousSolutions(current_period.id)
    chart = Chart(Solutions.query.filter_by(period_id=1).all(), users)
    return render_template('layout.html',
                           header=render_template('header.html', form=Login_form()),
                           main=render_template('admin-session.html', games=games, periods=periods),
                           footer=render_template('footer.html'),
                           script=chart.render())


@main.route('/4')
def index4():
    return render_template('layout.html',
                           header=render_template('header.html'),
                           main=render_template('album.html'),
                           footer=render_template('footer.html'))






@main.route('/8')
def index9():
    return render_template('layout.html',
                           header=render_template('header.html'),
                           main=render_template('partners.html'),
                           footer=render_template('footer.html'))


@main.route('/flush')
def flush():
    db.session.flush()
    return "True"

@main.route('/play')
@login_required
@gamer_required
def index10():
    period = Period.getActivePeriod(current_user.game_id)
    if period is not None:
        previous_solution = None
        game = Games.getGame(current_user.game_id)
        if period.period_number != 1:
            previous_solution = Solutions.getPreviousSolution(period, current_user.id)

        return render_template('layout.html',
                           header=render_template('header.html', form=Login_form()),
                           main=render_template('user-session.html', period=period, game=game, previous_solution=previous_solution),
                           footer=render_template('footer.html'),
                           script=render_template('users-script.html', game=game))
    return render_template('layout.html',
                           header=render_template('header.html', form=Login_form()),
                           footer=render_template('footer.html'))

@main.route('/result', methods=['POST'])
@login_required
@gamer_required
def result():
    model = Modeling(current_user, request.form)
    return "s"


# URL
@main.route('/news/add', methods=['POST'])
def add_news():
    try:
        temp = News(title=request.form['title'],
            text=request.form['text'],
            timestamp=request.form['date'],
            author_id=current_user.id)
        db.session.add(temp)
        db.session.commit()
        redirect('/news')
    except:
        pass

@main.route('/news/remove/<int:id>', methods=['POST'])
def remove_news(id):
    News.query.filter_by(id=id).delete()
    redirect('/news')

@main.route('/news')
def news_page():
    form = Login_form()
    return render_template('layout.html',
                           header=render_template('header.html', form=form),
                           main=render_template('news.html',
                                                isAdmin=current_user.isAdmin(),
                                                form=News_form(),
                                                news=News.query.all()),
                           footer=render_template('footer.html'))

@main.route('/galleries')
def galleries_page():
    return render_template('layout.html',
                           header=render_template('header.html'),
                           main=render_template('gallery.html'),
                           footer=render_template('footer.html'))

@main.route('/сontacts')
def contatst_page():
    return render_template('layout.html',
                           header=render_template('header.html'),
                           main=render_template('contacts.html'),
                           footer=render_template('footer.html'))

@main.route('/excel/<int:id>')
def get_logins_excel(id):
    Users=db.session.query(User.username,User.password_hash).filter_by(game_id=id).all()
    workbook = xlsxwriter.Workbook('users.xlsx')
    worksheet = workbook.add_worksheet()
    row = 1
    col = 0
    for item, cost in (Users):
        worksheet.write(row, col, item)
        worksheet.write(row, col + 1, cost)
        row += 1
    workbook.close()
    file_name = "users.xlsx"
    output = excel.make_response()
    output.headers["Content-Disposition"] = "attachment; filename=users.xlsx"
    output.headers["Content-type"] = "application/vnd.openxmlformats-\
    officedocument.spreadsheetml.sheet"
    return output