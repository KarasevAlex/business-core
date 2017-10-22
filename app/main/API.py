from . import main
from ..database import Partner, News, Team, Games, Solutions, Period
from .. import db, mail
from .modeling import Modeling
from flask import Flask, render_template, request
from flask import Flask, request, redirect, url_for
from werkzeug.utils import secure_filename
import uuid, os
from flask_login import current_user
from flask_mail import Message

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
    period = Period.query.filter_by(id=request.form['id']).first()
    period.isActive = request.form['isActive']
    db.session.add(period)

@main.route('/gallaries/photo/delete')
def gallaries_photo_delete():
    photos_id=request.form['delete']
    for photo in photos_id:
        pass

@main.route('/send/mail')
def send_mail():
    msg = Message("Hello",
                  sender="karasev_a_e@mail.ru",
                  recipients=["karasev_a_e@mail.ru"])
    mail.send(msg)

