from . import main
from .. import db, excel
from .chart import Chart
from .modeling import Modeling
from .decorators import admin_required, gamer_required
from .forms import Login as Login_form, News as News_form
from ..database import User, Games, Period, Solutions, News
from flask import render_template, request, flash, redirect
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
    games = Games.query.filter_by(id=id).first()
    users = User.query.filter_by(game_id=id).all()
    periods = Period.query.filter_by(game_id=id).all()
    last_active = None
    current_period = None
    for period in periods:
        if period.isFinished():
            last_active = period
        if period.check_period():
            current_period = period
    if last_active is not None:
        previous_solution = Solutions.getSolutions(last_active)
        chart = Chart()
        chart.generate(previous_solution, users)
    return render_template('layout.html',
                           header=render_template('header.html', form=Login_form()),
                           main=render_template('admin-session.html', games=games,
                                                periods=periods, last_active=last_active,
                                                current_period=current_period,
                                                previous_solution=previous_solution,
                                                users=users),
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
    if period['succeed']:
        previous_solution = None
        game = Games.getGame(current_user.game_id)
        period = period['data']
        if period.period_number != 1:
            previous_solution = Solutions.getPreviousSolution(period, current_user.id)

        return render_template('layout.html',
                           header=render_template('header.html', form=Login_form()),
                           main=render_template('user-session.html', period=period, game=game, previous_solution=previous_solution),
                           footer=render_template('footer.html')
                          )
    return render_template('layout.html',
                           header=render_template('header.html', form=Login_form()),
                           main=render_template('error.html', title=period['message'], message=period['time']),
                           footer=render_template('footer.html'))

@main.route('/result', methods=['POST'])
@login_required
@gamer_required
def result():
    if Period.check_period(request.form['period']):
        model = Modeling().generateGame(current_user, request.form)
        return render_template('layout.html',
                           header=render_template('header.html', form=Login_form()),
                           main=render_template('user-session.html', period=model.getPeriod(),
                                                game=model.getGame(),
                                                previous_solution=Solutions.getPreviousSolution(model.getPeriod(),
                                                                                                current_user.id),
                                                current_solution=model.getCurrentSolution()),
                           footer=render_template('footer.html'))
    return render_template('layout.html',
                           header=render_template('header.html', form=Login_form()),
                           main=render_template('error.html', message="Период завершен, решение не установлено"),
                           footer=render_template('footer.html'))



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
        return redirect('/news')
    except:
        pass

@main.route('/news/remove/<int:id>', methods=['POST'])
def remove_news(id):
    News.query.filter_by(id=id).delete()
    return redirect('/news')

@main.route('/news')
def news_page():
    return render_template('layout.html',
                           header=render_template('header.html', form=Login_form()),
                           main=render_template('news.html',
                                                isAdmin=current_user.isAdmin(),
                                                form=News_form(),
                                                news=News.query.all()),
                           footer=render_template('footer.html'))

@main.route('/galleries')
def galleries_page():
    return render_template('layout.html',
                           header=render_template('header.html',form=Login_form()),
                           main=render_template('gallery.html'),
                           footer=render_template('footer.html'))

@main.route('/сontacts')
def contatst_page():
    return render_template('layout.html',
                           header=render_template('header.html',form=Login_form()),
                           main=render_template('contacts.html'),
                           footer=render_template('footer.html'))

@main.route('/excel/<int:id>')
def get_excel(id):
    data = db.session.query(User.username, User.password_hash).filter_by(game_id=id).all()
    return excel.make_response_from_array(data, "xls")


@main.route('/demo')
def demo():
    return render_template('layout.html',
                           header=render_template('header.html', form=Login_form()),
                           main=render_template('demo-session.html', isResult=False),
                           footer=render_template('footer.html'))

@main.route('/demo/result', methods=['POST'])
def demo_result():
    # try:
    user_solution = Solutions()
    user_solution.update_solution(request.form)
    game = Games().create_default()
    user_solution.count_personal_params(game, isDemo=True)
    model = Modeling()
    model.generateDemo(user_solution, game)
    chart = Chart()
    chart.generateDemo(model.getCurrentSolutions())
    return render_template('layout.html',
                           header=render_template('header.html', form=Login_form()),
                           main=render_template('demo-session.html', isResult=True,

                                                game=model.getGame()),
                           footer=render_template('footer.html'),
                           script=chart.render())