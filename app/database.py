#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fileencoding=utf-8
from datetime import datetime
from . import db, loginManager
from flask_login import UserMixin
from datetime import datetime, timedelta
from flask import current_app, request, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from random import choice
from string import ascii_uppercase

@loginManager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# class Permission:
#     PLAY = 0x01
#     ADMINISTER = 0x80

#
# class Role(db.Model):
#     __tablename__ = 'roles'
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(64), unique=True)
#     default = db.Column(db.Boolean, default=False, index=True)
#     permissions = db.Column(db.Integer)
#     users = db.relationship('User', backref='role', lazy='dynamic')
#
#     @staticmethod
#     def insert_roles():
#         roles = {
#                 'Player': (Permission.PLAY, True),
#                 'Administrator': (0xff, False)
#         }
#         for r in roles:
#             role = Role.query.filter_by(name=r).first()
#             if role is None:
#                 role = Role(name=r)
#             role.permissions = roles[r][0]
#             role.default = roles[r][1]
#             db.session.add(role)
#         db.session.commit()
#




class User(db.Model, UserMixin):
    __tablename__ = 'users'
    __mapper_args__ = {"polymorphic_identity": "gamers"}
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role = db.Column(db.Integer)
    password_hash = db.Column(db.String(128))
    game_id = db.Column(db.Integer)
    name = db.Column(db.String(128))

    @property
    def password(self):
        raise AttributeError('Err')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password, salt_length=2)

    def verify_password(self, password):
        if self.role == 3 and self.password_hash == password:
            return True
        else:
            return check_password_hash(self.password_hash, password)

    def isAdmin(self):
        if self.role == 3:
            return False
        else:
            return True


    def generate(self, team_id):
        self.username = "g"+str(self.game_id)+"c"+str(team_id)
        self.password_hash = "g"+str(self.game_id)+"".join(choice(ascii_uppercase) for i in range(5))
        self.name = 'Team №'+str(team_id)
        self.role = 3

class News(db.Model):
    __tablename__ = 'News'
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    disabled = db.Column(db.Boolean)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))

class Games(db.Model):
    __tablename__ = 'games'
    #Идентификатор
    id = db.Column(db.Integer, primary_key=True)
    # Название
    title = db.Column(db.String(124))
    # Количество команд
    team_number = db.Column(db.Integer)
    # Количество периодов
    period_number = db.Column(db.Integer)
    # Начало и время периода
    time_start = db.Column(db.Time)
    time_duration = db.Column(db.Time)
    # Объем Рынков
    # СА
    sizeNA = db.Column(db.Integer)
    isSizeNA = db.Column(db.Boolean)
    # Европа
    sizeEurope = db.Column(db.Integer)
    isSizeEurope = db.Column(db.Boolean)
    # Азия
    sizeAsia = db.Column(db.Integer)
    isSizeAsia = db.Column(db.Boolean)

    # Доступные решения
    # Цена
    cost_active = db.Column(db.Boolean)
    cost_default = db.Column(db.Integer)
    cost_min = db.Column(db.Integer)
    cost_max = db.Column(db.Integer)
    # НИОКР (с/с)
    niokrSS_active = db.Column(db.Boolean)
    niokrSS_default = db.Column(db.Integer)
    niokrSS_min = db.Column(db.Integer)
    niokrSS_max = db.Column(db.Integer)
    # НИОКР (качество)
    niokrQuality_active = db.Column(db.Integer)
    niokrQuality_default = db.Column(db.Integer)
    niokrQuality_min = db.Column(db.Integer)
    niokrQuality_max = db.Column(db.Integer)

    #Заводы
    # СА
    NAFactory_active = db.Column(db.Boolean)
    NAFactory_default = db.Column(db.Integer)
    NAFactory_min = db.Column(db.Integer)
    NAFactory_max = db.Column(db.Integer)
    # Европа
    EuropeFactory_active = db.Column(db.Boolean)
    EuropeFactory_default = db.Column(db.Integer)
    EuropeFactory_min = db.Column(db.Integer)
    EuropeFactory_max = db.Column(db.Integer)
    # Азия
    AsiaFactory_active = db.Column(db.Boolean)
    AsiaFactory_default = db.Column(db.Integer)
    AsiaFactory_min = db.Column(db.Integer)
    AsiaFactory_max = db.Column(db.Integer)

    # Продвижение
    # СА
    NAPromotion_active = db.Column(db.Boolean)
    NAPromotion_default = db.Column(db.Integer)
    NAPromotion_min = db.Column(db.Integer)
    NAPromotion_max = db.Column(db.Integer)
    # Европа
    EuropePromotion_active = db.Column(db.Boolean)
    EuropePromotion_default = db.Column(db.Integer)
    EuropePromotion_min = db.Column(db.Integer)
    EuropePromotion_max = db.Column(db.Integer)
    # Азия
    AsiaPromotion_active = db.Column(db.Boolean)
    AsiaPromotion_default = db.Column(db.Integer)
    AsiaPromotion_min = db.Column(db.Integer)
    AsiaPromotion_max = db.Column(db.Integer)

    # Базовые параметры
    # Строительство завода
    costFactory = db.Column(db.Integer)
    amountFactory = db.Column(db.Integer)

    # Накладные расходы
    costOverheads = db.Column(db.Integer)
    amountOverheads = db.Column(db.Integer)

    # Расходы на демонтаж
    costDismantling = db.Column(db.Integer)
    amountDismantling = db.Column(db.Integer)

    # Бюджет команд
    teamBudget = db.Column(db.Integer)

    # Начальная с/с
    startSS1 = db.Column(db.Integer)
    startSS2 = db.Column(db.Integer)

    # Начальные вложения в с/с
    startAttachmentsSS1 = db.Column(db.Integer)
    startAttachmentsSS2 = db.Column(db.Integer)

    # Начальные вложения в качество
    startAttachmentsQuality1 = db.Column(db.Integer)
    startAttachmentsQuality2 = db.Column(db.Integer)

    # Степень в формуле с/с
    exponentSS1 = db.Column(db.Integer)
    exponentSS2 = db.Column(db.Integer)

    # Степень в формуле качества
    exponentQuality1 = db.Column(db.Integer)
    exponentQuality2 = db.Column(db.Integer)

    # Основание в формуле цены
    baseFormulaCost1 = db.Column(db.Integer)
    baseFormulaCost2 = db.Column(db.Integer)

    @staticmethod
    def create(form):
        try:
            game = Games(title=form['name'], team_number=form['team-number'], period_number=form['period-number'],
                         time_start=form['time-start'], time_duration=form['time-duration'],
                         costFactory=form['costFactory'], amountFactory=form['amountFactory'],
                         costOverheads=form['costOverheads'], amountOverheads=form['amountOverheads'],
                         costDismantling=form['costDismantling'], amountDismantling=form['amountDismantling'],
                         teamBudget=form['teamBudget'], startSS1=form['startSS1'], startSS2=form['startSS2'],
                         startAttachmentsSS1=form['startAttachmentsSS1'], startAttachmentsSS2=form['startAttachmentsSS2'],
                         startAttachmentsQuality1=form['startAttachmentsQuality1'],
                         startAttachmentsQuality2=form['startAttachmentsQuality2'],
                         exponentSS1=form['exponentSS1'], exponentSS2=form['exponentSS2'],
                         exponentQuality1=form['exponentQuality1'], exponentQuality2=form['exponentQuality2'],
                         baseFormulaCost1=form['baseFormulaCost1'], baseFormulaCost2=form['baseFormulaCost2']
                         )
            print(game.title)
            if 'cost' in form:
                game.cost_active = True
                game.cost_max = form['cost-max']
                game.cost_min = form['cost-min']
            else:
                game.cost_active = False
            game.cost_default = form['cost-default']

            if 'niokrSS' in form:
                game.niokrSS_active = True
                game.niokrSS_max = form['niokrSS-max']
                game.niokrSS_min = form['niokrSS-min']
            else:
                game.niokrSS_active = False
            game.niokrSS_default = form['niokrSS-default']

            if 'niokrQuality' in form:
                game.niokrQuality_active = True
                game.niokrQuality_max = form['niokrQuality-max']
                game.niokrQuality_min = form['niokrQuality-min']
            else:
                game.cost_active = False
            game.niokrQuality_default = form['niokrQuality-default']

            if 'isSizeNA' in form:
                game.isSizeNA = True
                game.sizeNA = form['sizeNA']

                if 'NAFactory' in form:
                    game.NAFactory_active = True
                    game.NAFactory_min = form['NAFactory-min']
                    game.NAFactory_max = form['NAFactory-max']
                else:
                    game.NAFactory_active = False
                game.NAFactory_default = form['NAFactory-default']

                if 'NAPromotion' in form:
                    game.NAPromotion_active = True
                    game.NAPromotion_min = form['NAPromotion-min']
                    game.NAPromotion_max = form['NAPromotion-max']
                else:
                    game.NAPromotion_active = False
                game.NAPromotion_default = form['NAPromotion-default']
            else:
                game.isSizeNA = False

            if 'isSizeEurope' in form:
                game.isSizeEurope = True
                game.sizeEurope = form['sizeEurope']
                if 'EuropeFactory' in form:
                    game.EuropeFactory_active = True
                    game.EuropeFactory_min = form['EuropeFactory-min']
                    game.EuropeFactory_max = form['EuropeFactory-max']
                else:
                    game.EuropeFactory_active = False
                game.EuropeFactory_default = form['EuropeFactory-default']

                if 'EuropePromotion' in form:
                    game.EuropePromotion_active = True
                    game.EuropePromotion_min = form['EuropePromotion-min']
                    game.EuropePromotion_max = form['EuropePromotion-max']
                else:
                    game.EuropePromotion_active = False
                game.EuropePromotion_default = form['EuropePromotion-default']

            else:
                game.isSizeEurope = False

            if 'isSizeAsia' in form:
                game.isSizeAsia = True
                game.sizeAsia = form['sizeAsia']
                if 'AsiaFactory' in form:
                    game.AsiaFactory_active = True
                    game.AsiaFactory_min = form['AsiaFactory-min']
                    game.AsiaFactory_max = form['AsiaFactory-max']
                else:
                    game.AsiaFactory_active = False
                game.AsiaFactory_default = form['AsiaFactory-default']

                if 'AsiaPromotion' in form:
                    game.AsiaPromotion_active = True
                    game.AsiaPromotion_min = form['AsiaPromotion-min']
                    game.AsiaPromotion_max = form['AsiaPromotion-max']
                else:
                    game.EuropePromotion_active = False
                game.AsiaPromotion_default = form['AsiaPromotion-default']
            else:
                game.isSizeAsia = False

            db.session.add(game)
            db.session.commit()
            for i in range(1,int(game.team_number)+1):
                gamer = User(game_id=game.id)
                gamer.generate(i)
                db.session.add(gamer)

            delta = timedelta(hours=game.time_duration.hour,
                              minutes=game.time_duration.minute,
                              microseconds=game.time_duration.microsecond)
            end_time = game.time_start
            for i in range(1, int(game.period_number) + 1):
                period = Period(game_id=game.id)
                period.generate(i, start_time=end_time, period_time=delta)
                end_time = period.period_end
                db.session.add(period)

        except ValueError as e:
            return e

    @staticmethod
    def getGame(game_id):
        return Games.query.filter_by(id=game_id).first()

class Period(db.Model):
    __tablename__ = 'periods'
    id = db.Column(db.Integer, primary_key=True)
    period_number = db.Column(db.Integer)
    period_start = db.Column(db.Time)
    period_end = db.Column(db.Time)
    period_duration = db.Column(db.Time)
    game_id = db.Column(db.Integer, db.ForeignKey('games.id'))


    def generate(self, period_number, start_time, period_time):
        self.period_number = period_number
        self.period_start = start_time
        self.period_end = (datetime.combine(datetime.now().date(), start_time) + period_time).time()
        self.period_duration = period_time

    @staticmethod
    def getActivePeriod(game_id):
        current_time = datetime.now().time()
        periods = Period.query.filter_by(game_id=game_id)
        for period in periods:
            if current_time >= period.period_start and current_time <= period.period_end:
                return period

class Solutions(db.Model):
    __tablename__ = 'solutions'
    id = db.Column(db.Integer, primary_key=True)
    period_id = db.Column(db.Integer, db.ForeignKey('periods.id'))
    gamer_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    cost = db.Column(db.Integer)
    niokrSS = db.Column(db.Integer)
    niokrQuality = db.Column(db.Integer)
    NAFactory = db.Column(db.Integer)
    EuropeFactory = db.Column(db.Integer)
    AsiaFactory = db.Column(db.Integer)
    NAPromotion = db.Column(db.Integer)
    EuropePromotion = db.Column(db.Integer)
    AsiaPromotion = db.Column(db.Integer)

class Results(db.Model):
    __tablename__ = 'results'
    id = db.Column(db.Integer, primary_key=True)
    solutions_id = db.Column(db.Integer, db.ForeignKey('solutions.id'))
    # Расходы
    Budget = db.Column(db.Integer)
    # Спрос
    Demand_NA = db.Column(db.Integer)
    Demand_Europa = db.Column(db.Integer)
    Demand_Asia = db.Column(db.Integer)
    # Объем продаж
    Sales_NA = db.Column(db.Integer)
    Sales_Europa = db.Column(db.Integer)
    Sales_Asia = db.Column(db.Integer)
    # Себестоимость продукции
    Prime_cost = db.Column(db.Integer)
    # Прибыль в периоде
    Profit = db.Column(db.Integer)


