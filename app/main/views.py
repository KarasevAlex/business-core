from . import main
from .. import db
from .modeling import Modeling
from .decorators import admin_required, gamer_required
from .forms import Login as Login_form
from ..database import User, Games, Period, Solutions, Results
from flask import render_template, request, flash,redirect
from flask_login import login_user, logout_user, login_required, current_user


@main.route('/create_database', methods=['GET', 'POST'])
def create_database():
    # try:
    db.create_all()
    db.session.add(User(username='Admin', password='Admin', role=1))
    return "succed"
    # except Exception as e:
    #     return "fail"

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
    е = current_user
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
                           header=render_template('header.html'),
                           main=render_template('admin-list.html', games=games),
                           footer=render_template('footer.html'))


@main.route('/game/<int:id>')
@login_required
def session_admin(id):
    games = Games.query.filter_by(id=id)
    periods = Period.query.filter_by(game_id=id)
    return render_template('layout.html',
                           header=render_template('header.html'),
                           main=render_template('admin-session.html', games=games, periods=periods),
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
        game = Games.getGame(current_user.game_id)

        return render_template('layout.html',
                           header=render_template('header.html'),
                           main=render_template('user-session.html', period=period, game=game),
                           footer=render_template('footer.html'))
    return render_template('layout.html',
                           header=render_template('header.html'),
                           footer=render_template('footer.html'))

@main.route('/result', methods=['POST'])
@login_required
@gamer_required
def result():
    model = Modeling(current_user, request.form)
    print(1)
    # # Решения за другие периоды
    # solutions = Solutions.query.filter_by(gamer_id=current_user.id).all()
    # # Решения за прошлы периоды, нахуя только
    # results = Results.query.filter_by(gamer_id=current_user.id).all()
    # # исходные данные
    # game = Games.getGame(current_user.game_id)
    # # решение для текущего периода
    # solution = Solutions(gamer_id=current_user.id)
    # solution.generate(request.form, game)
    # # Результаты по текущему периоду
    # result = Results()
    # Solutions.getPreviousSolutions(current_user.id, 2)
    # result.recount(current_solution=solution,
    #                            game=game,
    #                            solutions=solutions,
    #                            results=results)
    # db.session.add(solution)
    # db.session.add(result)
    return "s"


