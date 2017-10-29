from . import main
from ..database import Partner, News, Team, Games, Solutions, Period, Gallery, Photos
from .. import db, mail
from .modeling import Modeling
from .decorators import admin_required, gamer_required
from flask import Flask, request, redirect, url_for
from flask_api import status
from werkzeug.utils import secure_filename
import uuid, os, json
from flask_login import current_user
from flask_mail import Message

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
    temp = News(title=request.form['title'],
        text=request.form['text'],
        timestamp=request.form['date'],
        author_id=current_user.id)
    db.session.add(temp)
    db.session.commit()
    return redirect('/news')

@main.route('/news/remove/<int:id>', methods=['POST'])
def remove_news(id):
    News.query.filter_by(id=id).delete()
    return redirect('/news')



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

    return redirect('/galleries')

def gallaries_get_dict():
    LastPost = db.aliased(Photos, name='last')
    last_id = (
        db.session.query(LastPost.id)
            .filter(LastPost.gallery_id == Gallery.id)
            .order_by(LastPost.id.desc())
            .limit(1)
            .correlate(Gallery)
            .as_scalar()
    )
    return db.session.query(Gallery, Photos).outerjoin(Photos, Photos.id == last_id).all()

@main.route('/gallery/remove/<int:id>')
@admin_required
def gallery_remove(id):
    try:
        obj = Photos.query.filter_by(gallery_id=id).all()
        for ob in obj:
            if remove_fite(ob.path):
                db.session.delete(ob)
        Gallery.query.filter_by(id=id).delete()
        return status.HTTP_200_OK
    except:
        return status.HTTP_500_INTERNAL_SERVER_ERROR


@main.route('/gallery/photo/remove/<int:id>')
@admin_required
def gallery_photo_remove(id):
    try:
        obj = Photos.query.filter_by(id=id).first()
        if remove_fite(obj.path):
            db.session.delete(obj)
        return status.HTTP_200_OK
    except:
        return status.HTTP_500_INTERNAL_SERVER_ERROR

@main.route('/news/remove/<int:id>')
@admin_required
def news_remove(id):
    try:
        News.query.filter_by(id=id).delete()
        return status.HTTP_200_OK
    except:
        return status.HTTP_500_INTERNAL_SERVER_ERROR

@main.route('/partner/remove/<int:id>')
@admin_required
def partner_remove(id):
    try:
        obj = Partner.query.filter_by(id=id).first()
        if remove_fite(obj.picture):
            db.session.delete(obj)
        return status.HTTP_200_OK
    except:
        return status.HTTP_500_INTERNAL_SERVER_ERROR


@main.route('/send/mail')
def send_mail():
    msg = Message("Hello",
                  sender="karasev_a_e@mail.ru",
                  recipients=["karasev_a_e@mail.ru"])
    mail.send(msg)

