from . import main, API
from .. import db, excel
from .chart import Chart
from .modeling import Modeling
from .decorators import admin_required, gamer_required
from .forms import Login as Login_form, News as News_form
from ..database import User, Games, Period, Solutions, News, Partner, Team, StaticPages
from flask import render_template, request, flash, redirect
from flask_login import login_user, logout_user, login_required, current_user


@main.route('/create_database', methods=['GET', 'POST'])
def create_database():

        db.create_all()
        print('1')
        db.session.add(User(username='Admin', password='Admin', role=1))
        return "succed"

        return "fail"

@main.route('/', methods=['POST','GET'])
def index():
    return redirect('/team')

@main.route('/login', methods=['POST'])
def index_():
    form = Login_form()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.login.data).first()
        if user is not None:
            if user.verify_password(form.password.data):
                if user.role == 3:
                    login_user(user, remember=True)
                    return redirect('/play/1')
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

@main.route('/game/<int:id>/<int:period_id>')
@login_required
def session_admin(id, period_id):
    games = Games.query.filter_by(id=id).first()
    users = User.query.filter_by(game_id=id).all()
    periods = Period.query.filter_by(game_id=id).all()
    period = Period.query.filter_by(period_number=period_id, game_id=id).first()
    current_period = Period.getActivePeriod(id)
    if current_period['succeed']:
        current_period = current_period['data']
    else:
        current_period = None
    period_solution = None
    if period.isFinished():
        period_solution = db.session.query(User,Solutions).\
            outerjoin(Solutions, User.id == Solutions.gamer_id).\
            filter(Solutions.period_id == period.id).all()
        # period_solution =
        chart = Chart()
        chart.generate(Solutions.getSolutions(period), users)
        return render_template('layout.html',
                               header=render_template('header.html', form=Login_form()),
                               main=render_template('admin-session.html', games=games,
                                                    periods=periods, period=period,
                                                    current_period=current_period,
                                                    previous_solution=period_solution,
                                                    users=users),
                               footer=render_template('footer.html'),
                               script=chart.render())
    return render_template('layout.html',
                           header=render_template('header.html', form=Login_form()),
                           main=render_template('admin-session.html', games=games,
                                                periods=periods, period=period,
                                                current_period=current_period,
                                                previous_solution=period_solution,
                                                users=users),
                           footer=render_template('footer.html'))
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

@main.route('/play/<int:period_result>',methods=['POST', 'GET'])
@login_required
@gamer_required
def user_game(period_result):
    period = Period.getActivePeriod(current_user.game_id)
    users = User.query.filter_by(game_id=current_user.game_id).all()
    previous_solution = None
    results = None
    pResult = Period.getPeriod(current_user.game_id, period_result)
    if request.method == "GET":
        if period['succeed']:
            game = Games.getGame(current_user.game_id)
            period = period['data']
            if period.period_number != 1:
                previous_solution = Solutions.getPreviousSolution(period, current_user.id)
                if Solutions.isSolutionAllowed(period, period_result):
                    results = Solutions.getSolutions(pResult)
                    chart = Chart()
                    chart.generate(results, users)
                    return render_template('layout.html',
                                           header=render_template('header.html', form=Login_form()),
                                           main=render_template('user-session.html', period=period,
                                                                game=game, users=users,
                                                                previous_solution=previous_solution,
                                                                results=results, period_result=pResult),
                                           footer=render_template('footer.html'),
                                           script=chart.render())
            return render_template('layout.html',
                                   header=render_template('header.html', form=Login_form()),
                                   main=render_template('user-session.html', period=period,
                                                        game=game, users=users,
                                                        previous_solution=previous_solution,
                                                        results=results, period_result=pResult),
                                   footer=render_template('footer.html'))
        return render_template('layout.html',
                               header=render_template('header.html', form=Login_form()),
                               main=render_template('error.html', title=period['message'], message=period['time']),
                               footer=render_template('footer.html'))
    else:
        if Period.check_period_by_id(request.form['period']):
            model = Modeling()
            model.generateGame(current_user, request.form)

            if period['data'].period_number != 1 and Solutions.isSolutionAllowed(period, period_result):
                results = Solutions.getSolutions(pResult)
                chart = Chart()
                chart.generate(results, users)
                return render_template('layout.html',
                                       header=render_template('header.html', form=Login_form()),
                                       main=render_template('user-session.html', period=model.getPeriod(),
                                                            game=model.getGame(), users=users,
                                                            previous_solution=Solutions.getPreviousSolution(
                                                                model.getPeriod(),
                                                                current_user.id),
                                                            results=results, period_result=pResult,
                                                            current_solution=model.getCurrentSolution()),
                                       footer=render_template('footer.html'),
                                       script=chart.render())
            return render_template('layout.html',
                                   header=render_template('header.html', form=Login_form()),
                                   main=render_template('user-session.html', period=model.getPeriod(),
                                                        game=model.getGame(), users=users,
                                                        previous_solution=Solutions.getPreviousSolution(
                                                            model.getPeriod(),
                                                            current_user.id),
                                                        results=results, period_result=pResult,
                                                        current_solution=model.getCurrentSolution()),
                                   footer=render_template('footer.html'))
        return render_template('layout.html',
                               header=render_template('header.html', form=Login_form()),
                               main=render_template('error.html', message="Период завершен, решение не установлено"),
                               footer=render_template('footer.html'))



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
                                                previous_solution=model.getCurrentSolutions(),
                                                game=model.getGame()),
                           footer=render_template('footer.html'),
                           script=chart.render())




@main.route('/period/<int:id>', methods=['POST'])
def change_period(id):
    try:
        period = Period.query.filter_by(id=id).first()
        period.changePeriod(request.form['begin'], request.form['period'], request.form['end'])
        db.session.add(period)
        return redirect('/game/%s' % period.game_id)
    except:
        return render_template('layout.html',
                               header=render_template('header.html', form=Login_form()),
                               main=render_template('error.html', message="Произошла ошибка повторите запрос позже"),
                               footer=render_template('footer.html'))

@main.route('/team')
def team_page():
    try:
        return render_template('layout.html',
                               header=render_template('header.html', form=Login_form()),
                               main=render_template('index.html',
                                                    members=Team.query.all(),
                                                    isAdmin=current_user.isAdmin()))
    except:
        return render_template('layout.html',
                               header=render_template('header.html', form=Login_form()),
                               main=render_template('error.html', message="Произошла ошибка повторите запрос позже"),
                               footer=render_template('footer.html'))

@main.route('/partners')
def partners_page():
    try:
        return render_template('layout.html',
                               header=render_template('header.html', form=Login_form()),
                               main=render_template('partners.html',
                                                    partners=Partner.query.all(),
                                                    isAdmin=current_user.isAdmin()),
                               footer=render_template('footer.html'))
    except:
        return render_template('layout.html',
                               header=render_template('header.html', form=Login_form()),
                               main=render_template('error.html', message="Произошла ошибка повторите запрос позже"),
                               footer=render_template('footer.html'))

@main.route('/<string:page>')
def static_page(page):
    pages = ['decription', 'organizations', 'students']
    if page in pages:
        page = StaticPages.query.filter_by(page_url=page).first()
        return render_template('layout.html',
                       header=render_template('header.html', form=Login_form()),
                       main=render_template('static.html', page=page,
                                            isAdmin=current_user.isAdmin()),
                       footer=render_template('footer.html'))
