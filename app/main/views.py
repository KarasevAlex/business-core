from . import main, API
from .. import db, excel
from .chart import Chart
from .modeling import Modeling
from .decorators import admin_required, gamer_required
from .forms import Login as Login_form, News as News_form
from ..database import User, Games, Period, Solutions, News, Partner, Team, StaticPages, Gallery, Photos
from flask import render_template, request, flash, redirect, send_from_directory
from flask_login import login_user, logout_user, login_required, current_user
import os



@main.route('/create_database', methods=['GET', 'POST'])
def create_database():
    try:
        db.create_all()
        print('1')
        db.session.add(User(username='Admin', password='Admin', role=1))
        return "succed"
    except:
        return "fail"

@main.route('/', methods=['POST','GET'])
def index():
    return redirect('/team')

@main.route('/game/page/<int:page>', methods=['POST', 'GET'])
@login_required
@admin_required
def index2(page):
    if request.method == "POST":
        Games.create(request.form)
    pagination = Games.query.order_by(Games.date_start.desc()).paginate(
            page, per_page=5, error_out=False)
    return render_template('layout.html',
                           header=render_template('header.html', form=Login_form(), isAdmin=current_user.isAdmin()),
                           main=render_template('admin-list.html', games=pagination.items,pagination=pagination),
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
        period_solution = db.session.query(User, Solutions).\
            outerjoin(Solutions, User.id == Solutions.gamer_id).\
            filter(Solutions.period_id == period.id).all()
        chart = Chart()
        chart.generate(Solutions.getSolutions(period), users)
        return render_template('layout.html',
                               header=render_template('header.html', form=Login_form(),  isAdmin=current_user.isAdmin()),
                               main=render_template('admin-session.html', games=games,
                                                    periods=periods, period=period,
                                                    current_period=current_period,
                                                    previous_solution=period_solution,
                                                    users=users),
                               footer=render_template('footer.html'),
                               script=chart.render())
    return render_template('layout.html',
                           header=render_template('header.html', form=Login_form(),  isAdmin=current_user.isAdmin()),
                           main=render_template('admin-session.html', games=games,
                                                periods=periods, period=period,
                                                current_period=current_period,
                                                previous_solution=period_solution,
                                                users=users),
                           footer=render_template('footer.html'))

@main.route('/flush')
def flush():
    db.session.flush()
    return "True"

# @main.route('/play/<int:period_result>',methods=['GET'])
# @login_required
# @gamer_required
# def user_game(period_result):
#     period = Period.getActivePeriod(current_user.game_id)
#     users = User.query.filter_by(game_id=current_user.game_id).all()
#     previous_solution = None
#     results = None
#     pResult = Period.getPeriod(current_user.game_id, period_result)
#     if period['succeed']:
#         game = Games.getGame(current_user.game_id)
#         period = period['data']
#         if period.period_number != 1:
#             previous_solution = Solutions.getPreviousSolution(period, current_user.id)
#             if Solutions.isSolutionAllowed(period, period_result):
#                 results = Solutions.getSolutions(pResult)
#                 chart = Chart()
#                 chart.generate(results, users)
#                 return render_template('layout.html',
#                                        header=render_template('header.html', form=Login_form(),  isAdmin=current_user.isAdmin()),
#                                        main=render_template('user-session.html', period=period,
#                                                             game=game, users=users,
#                                                             previous_solution=previous_solution,
#                                                             results=results, period_result=pResult),
#                                        footer=render_template('footer.html'),
#                                        script=chart.render())
#         return render_template('layout.html',
#                                header=render_template('header.html', form=Login_form(),  isAdmin=current_user.isAdmin()),
#                                main=render_template('user-session.html', period=period,
#                                                     game=game, users=users,
#                                                     previous_solution=previous_solution,
#                                                     results=results, period_result=pResult),
#                                footer=render_template('footer.html'))
#     return render_template('layout.html',
#                            header=render_template('header.html', form=Login_form(),  isAdmin=current_user.isAdmin()),
#                            main=render_template('error.html', title=period['message'], message=period['time']),
#                            footer=render_template('footer.html'))
@main.route('/play/<int:period_result>',methods=['GET'])
@login_required
@gamer_required
def user_game(period_result):
    users = None
    previous_solution = None
    game = None
    chart = Chart()
    requiredResult = None
    requiredPeriod = Period.query.filter_by(game_id=current_user.game_id, period_number=period_result).one()
    if Solutions.isSolutionsAllowed(game_id=current_user.game_id, period_number=period_result):
        requiredResult = Solutions.getSolutions(requiredPeriod)
        users = User.query.filter_by(game_id=current_user.game_id).all()
        chart = Chart()
        chart.generate(requiredResult, users)
    activePeriod = Period.getActivePeriodVer2(current_user.game_id)
    if activePeriod is not None:
        game = Games.getGame(current_user.game_id)
        previous_solution = Solutions.getPreviousSolution(activePeriod, current_user.id)

    return render_template('layout.html',
                           header=render_template('header.html', form=Login_form(),  isAdmin=current_user.isAdmin()),
                           main=render_template('user-sessionV2.html', activePeriod=activePeriod,
                                                game=game, users=users,
                                                previousSolution=previous_solution,
                                                results=requiredResult, requiredPeriod=requiredPeriod),
                           footer=render_template('footer.html'),
                           script=chart.render())


@main.route('/play/<int:period_result>', methods=['POST'])
@login_required
@gamer_required
def set_game_solution(period_result):
    if Period.check_period_by_id(request.form['period']):
        model = Modeling()
        model.generateGame(current_user, request.form)
    return redirect('/play/%s' % period_result)

@main.route('/news/page/<int:page>')
def news_page(page):
    pagination = News.query.order_by(News.timestamp.desc()).paginate(
        page, per_page=5, error_out=False)
    return render_template('layout.html',
                           header=render_template('header.html',
                                                  form=Login_form(),
                                                  isAdmin=current_user.isAdmin(),
                                                  news_page="active"
                                                  ),
                           main=render_template('news.html',
                                                isAdmin=current_user.isAdmin(),
                                                form=News_form(),
                                                news=pagination.items, pagination=pagination),
                           footer=render_template('footer.html'))

@main.route('/galleries/page/<int:page>')
def galleries_page(page):
    pagination = API.gallaries_get_dict(page)
    return render_template('layout.html',
                           header=render_template('header.html',
                                                  form=Login_form(),
                                                  isAdmin=current_user.isAdmin(),
                                                  galleries_page="active"
                                                  ),
                           main=render_template('gallery.html',
                                                gallaries=pagination.items,
                                                pagination=pagination),
                           footer=render_template('footer.html'))

@main.route('/galleries/<int:id>/page/<int:page>')
def gallery_page(id, page):
    pagination = Photos.query.filter_by(gallery_id=id).paginate(
        page, per_page=6, error_out=False)
    return render_template('layout.html',
                           header=render_template('header.html',
                                                  form=Login_form(),
                                                  isAdmin=current_user.isAdmin(),
                                                  galleries_page="active"
                                                  ),
                           main=render_template('album.html',
                                                gallary=Gallery.query.filter_by(id=id).first(),
                                                photos=pagination.items,
                                                pagination=pagination),
                           footer=render_template('footer.html'))

@main.route('/сontacts')
def contatst_page():
    return render_template('layout.html',
                           header=render_template('header.html',
                                                  form=Login_form(),
                                                  isAdmin=current_user.isAdmin(),
                                                  contacts_page="active"
                                                  ),
                           main=render_template('contacts.html'),
                           footer=render_template('footer.html'))

@main.route('/excel/<int:id>')
def get_excel(id):
    data = db.session.query(User.username, User.password_hash).filter_by(game_id=id).all()
    return excel.make_response_from_array(data, "xls")


@main.route('/demo')
def demo():
    return render_template('layout.html',
                           header=render_template('header.html',
                                                  form=Login_form(),
                                                  isAdmin=current_user.isAdmin(),
                                                  demo_page="active"
                                                  ),
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
                           header=render_template('header.html', form=Login_form(),  isAdmin=current_user.isAdmin()),
                           main=render_template('demo-session.html', isResult=True,
                                                previous_solution=model.getCurrentSolutions(),
                                                game=model.getGame()),
                           footer=render_template('footer.html'),
                           script=chart.render())


@main.route('/team')
def team_page():
    try:
        return render_template('layout.html',
                               header=render_template('header.html',
                                                      form=Login_form(),
                                                      about_page="active"),
                               main=render_template('index.html',
                                                    members=Team.query.filter_by(type=0).all(),
                                                    isAdmin=current_user.isAdmin()))
    except:
        return render_template('layout.html',
                               header=render_template('header.html', form=Login_form(), isAdmin=current_user.isAdmin()),
                               main=render_template('error.html', message="Произошла ошибка повторите запрос позже"),
                               footer=render_template('footer.html'))
@main.route('/recommendation')
def recommendation_page():
    try:
        return render_template('layout.html',
                               header=render_template('header.html',
                                                      form=Login_form(),
                                                      about_page="active"),
                               main=render_template('recommendation.html',
                                                    members=Team.query.filter_by(type=1).all(),
                                                    isAdmin=current_user.isAdmin()))
    except:
        return render_template('layout.html',
                               header=render_template('header.html', form=Login_form(), isAdmin=current_user.isAdmin()),
                               main=render_template('error.html', message="Произошла ошибка повторите запрос позже"),
                               footer=render_template('footer.html'))

@main.route('/partners')
def partners_page():
    try:
        return render_template('layout.html',
                               header=render_template('header.html',
                                                      form=Login_form(),
                                                      isAdmin=current_user.isAdmin(),
                                                      about_page="active"),
                               main=render_template('partners.html',
                                                    partners=Partner.query.all(),
                                                    isAdmin=current_user.isAdmin()),
                               footer=render_template('footer.html'))
    except:
        return render_template('layout.html',
                               header=render_template('header.html', form=Login_form(), isAdmin=current_user.isAdmin()),
                               main=render_template('error.html', message="Произошла ошибка повторите запрос позже"),
                               footer=render_template('footer.html'))

@main.route('/<string:page>')
def static_page(page):
    pages = ['decription', 'organizations', 'students', 'services']
    if page in pages:
        page_obj = StaticPages.query.filter_by(page_url=page).first()
        return render_template('layout.html',
                       header=render_template('header.html',
                                              form=Login_form(),
                                              isAdmin=current_user.isAdmin(),
                                              about_page="active"),
                       main=render_template('static.html', page=page_obj,
                                            isAdmin=current_user.isAdmin(),
                                            page_name=page),
                       footer=render_template('footer.html'))


@main.route('/helps')
def helps_page():
    return render_template('layout.html',
                   header=render_template('header.html',
                                          form=Login_form(),
                                          isAdmin=current_user.isAdmin(),
                                          about_page="active"),
                   main=render_template('helps.html',
                                        isAdmin=current_user.isAdmin()),
                   footer=render_template('footer.html'))


@main.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(main.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')
@main.route('/401')
def custom_401():
    return render_template('layout.html',
                           header=render_template('header.html', form=Login_form(), isAdmin=current_user.isAdmin()),
                           main=render_template('error.html', title="Ошибка доступа"),
                           footer=render_template('footer.html'))
@main.route('/404')
def custom_404():
    return render_template('layout.html',
                           header=render_template('header.html', form=Login_form(), isAdmin=current_user.isAdmin()),
                           main=render_template('error.html', title="Запрашиваемая страница не найдена"),
                           footer=render_template('footer.html'))
@main.route('/500')
def custom_500():
    return render_template('layout.html',
                           header=render_template('header.html', form=Login_form(), isAdmin=current_user.isAdmin()),
                           main=render_template('error.html', title="Внутренняя ошибка сервера"),
                           footer=render_template('footer.html'))
