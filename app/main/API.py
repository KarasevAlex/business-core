from . import main
from ..database import Partner, News, Team, Games, Solutions, Period, Gallery, Photos, User, StaticPages
from .. import db, mail
from .modeling import Modeling
from .decorators import admin_required
from flask import request, redirect, render_template, abort
from flask_api import status
from werkzeug.utils import secure_filename
import uuid, os, json
from flask_mail import Message
from flask_login import login_user, logout_user, login_required, current_user
from .forms import Login as Login_form
from datetime import datetime, timedelta

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif', 'JPG'])

def allowed_filename(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

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

def remove_fite(filnename):
    try:
        mypath = main.root_path[:-4] + '/static/img/picturs/' + filnename
        os.remove(mypath)
        return  True
    except:
        return False

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
        member = Team(picture=filename, name=request.form['name'], type=0, discription=request.form['description'])
        db.session.add(member)
        return redirect('/team')

@main.route('/member/remove/<int:id>', methods=['GET'])
def member_remove(id):
    obj = Team.query.filter_by(id=id).first()
    mypath = main.root_path[:-4] + '/static/img/picturs/' + obj.picture
    os.remove(mypath)
    db.session.delete(obj)
    return redirect('/team')

@main.route('/recommendation/add', methods=['POST'])
def recommendation_add():
    filename = upload(request.files['file'])
    if filename is not None:
        member = Team(picture=filename, name=request.form['name'], type=1, discription=request.form['description'])
        db.session.add(member)
        return redirect('/team')



@main.route('/news/add', methods=['POST'])
def add_news():
    temp = News(title=request.form['title'],
        text=request.form['text'],
        timestamp=request.form['date'],
        author_id=current_user.id)
    db.session.add(temp)
    db.session.commit()
    return redirect('/news/page/1')

@main.route('/games/remove/<int:id>',  methods=['POST'])
@admin_required
def geme_remove(id):
    # try:
    db.session.delete(Games.query.filter_by(id=id).one())
    return '', status.HTTP_200_OK

@main.route('/game/<int:id>/period/add',  methods=['get'])
def geme_period_add(id):
    game = Games.query.filter_by(id=id).one()
    last = Period.query.filter_by(game_id=id).order_by(db.desc(Period.period_number)).limit(1).one()

    newPeriod = Period(game_id=game.id)
    newPeriod.generate(
                     period_number=last.period_number+1,
                     start_time=last.period_end,
                     period_time=game.time_duration)
    db.session.add(newPeriod)
    db.session.commit()
    return redirect('/game/%s/1' % id)


@main.route('/game/finish/<int:id>', methods=['POST'])
def finish_game(id):
    game = Games.query.filter_by(id=id).first()
    game.isFinished = True
    db.session.add(game)
    return redirect('/game/%s/1'% id)


@main.route('/solutions/change', methods=['POST'])
def solutions_change():
    form = request.form
    solutions = Solutions.query.filter_by(period_id=form['period-id']).all()
    game = Games.getGame(form['game-id'])
    for solution in solutions:
        solution.cost = form[str(solution.gamer_id)+'-cost']
        solution.NAFactory = form[str(solution.gamer_id)+'-NAFactory']
        solution.EuropeFactory = form[str(solution.gamer_id)+'-EuropeFactory']
        solution.AsiaFactory = form[str(solution.gamer_id)+'-AsiaFactory']
        solution.NAPromotion = form[str(solution.gamer_id)+'-NAPromotion']
        solution.EuropePromotion = form[str(solution.gamer_id)+'-EuropePromotion']
        solution.AsiaPromotion = form[str(solution.gamer_id)+'-AsiaPromotion']
        solution.niokrSS = form[str(solution.gamer_id) + '-niokrSS']
        solution.niokrQuality = form[str(solution.gamer_id) + '-niokrQuality']
        solution.count_personal_params(game)

    modeling = Modeling()
    modeling.adminRecount(form['period-id'],game)
    return redirect('/game/%s/%s' % (form['game-id'], form['period-number']))

@main.route('/period/status', methods=['POST'])
def change_period_status():
    try:
        period = Period.query.filter_by(id=request.form['id']).first()
        temp_sheet = request.form['isActive']
        if request.form['isActive'] == 'true':
            period.isActive = True
            db.session.add(period)
            return json.dumps(True)
        period.isActive = False
        db.session.add(period)
        return json.dumps(True)
    except:
        return json.dumps(False)

@main.route('/period/<int:id>', methods=['POST'])
def change_period(id):
    try:
        period = Period.query.filter_by(id=id).first()
        period.changePeriod(request.form['begin'], request.form['period'], request.form['end'])
        db.session.add(period)
        return redirect('/game/%s/1' % period.game_id)
    except:
        return render_template('layout.html',
                               header=render_template('header.html', form=Login_form(), isAdmin=current_user.isAdmin()),
                               main=render_template('error.html', message="Произошла ошибка повторите запрос позже"),
                               footer=render_template('footer.html'))

@main.route('/gallaries/photo/delete')
def gallaries_photo_delete():
    photos_id = request.form['delete']
    for photo in photos_id:
        pass



@main.route('/gallaries/add', methods=['POST'])
def gallaries_add():
    gallery = Gallery(title=request.form['title'])
    db.session.add(gallery)
    db.session.commit()
    for file in request.files.getlist('file'):
        filename = upload(file)
        if filename is not None:
            photo = Photos(gallery_id=gallery.id, path=filename)
            db.session.add(photo)

    return redirect('/galleries/page/1')

def gallaries_get_dict(page):
    LastPost = db.aliased(Photos, name='last')
    last_id = (
        db.session.query(LastPost.id)
            .filter(LastPost.gallery_id == Gallery.id)
            .order_by(LastPost.id.desc())
            .limit(1)
            .correlate(Gallery)
            .as_scalar()
    )
    return db.session.query(Gallery, Photos).outerjoin(Photos, Photos.id == last_id).paginate(
            page, per_page=4, error_out=False)


@main.route('/gallery/remove/<int:id>', methods=['POST','GET'])
def gallery_remove(id):
    try:
        obj = Photos.query.filter_by(gallery_id=id).all()
        for ob in obj:
            if remove_fite(ob.path):
                db.session.delete(ob)
        db.session.delete(Gallery.query.filter_by(id=id).one())
        return '', status.HTTP_200_OK
    except:
        abort(status.HTTP_500_INTERNAL_SERVER_ERROR)


@main.route('/gallery/photo/remove/<int:id>')
@admin_required
def gallery_photo_remove(id):
    try:
        obj = Photos.query.filter_by(id=id).first()
        if remove_fite(obj.path):
            db.session.delete(obj)
        return '', status.HTTP_200_OK
    except:
        abort(status.HTTP_500_INTERNAL_SERVER_ERROR)

@main.route('/gallery/poster', methods=['POST'])
@admin_required
def gallery_poster():
    try:
        photo = Photos.query.filter_by(id=request.form['id'])
        gal = Gallery.query.filter_by(id=photo.gallary_id).firts()
        gal.Poster = photo.id
        db.session.add(gal)
        return '', status.HTTP_200_OK
    except:
        abort(status.HTTP_500_INTERNAL_SERVER_ERROR)


@main.route('/gallery/photo/add', methods=['POST'])
@admin_required
def gallery_photo_add():
    filename = upload(request.files['file'])
    if filename is not None:
        photos = Photos(path=filename, gallery_id=request.form['id'])
        db.session.add(photos)
        return redirect('/galleries/%s' % request.files['id'])


@main.route('/news/remove/<int:id>', methods=['POST'])
@admin_required
def news_remove(id):
    try:
        News.query.filter_by(id=id).delete()
        return '', status.HTTP_200_OK
    except:
        abort(status.HTTP_500_INTERNAL_SERVER_ERROR)

@main.route('/partner/remove/<int:id>')
@admin_required
def partner_remove(id):
    try:
        obj = Partner.query.filter_by(id=id).first()
        if remove_fite(obj.picture):
            db.session.delete(obj)
        return '', status.HTTP_200_OK
    except:
        abort(status.HTTP_500_INTERNAL_SERVER_ERROR)


@main.route('/send/mail')
def send_mail():
    with mail.connect() as conn:
        msg = Message("Hello",
                      sender='',
                      recipients=["karasev_a_e@mail.ru"])
        conn.send(msg)

    return "", 200


@main.route('/static')
def insert_static_page():
    pages = {'decription': 'Краткое описание',
             'organizations': 'Образовательным учереждениям',
             'students': 'Учащимся',
             'services': 'Цены и услуги'}
    for url in pages.keys():
         db.session.add(StaticPages(title=pages[url], page_url=url, text="hjgjhghg"))
    return '', 200


@main.route('/static/edit/<int:id>', methods=['POST'])
def edit_static_page(id):
    page = StaticPages.query.filter_by(id=id).one()
    page.text = request.form['description']
    db.session.add(page)
    db.session.commit()
    return redirect('/%s'% page.page_url)


@main.route('/login', methods=['POST'])
def index_():
    form = Login_form()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.login.data).first()
        if user is not None:
            if user.verify_password(form.password.data):
                if user.role == 3:
                    login_user(user, remember=True)
                    return '/play/1'
                else:
                    login_user(user, remember=True)
                    return '/game/page/1'
    abort(500)

@main.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')

