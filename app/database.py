#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fileencoding=utf-8

from . import db, loginManager
from flask_login import UserMixin
from datetime import datetime, timedelta
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
    __tablename__ = 'news'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text)
    body = db.Column(db.Text)
    timestamp = db.Column(db.Date, index=True, default=datetime.utcnow)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self, title, text, timestamp, author_id):
        super().__init__()
        self.title = title
        self.body = text
        self.timestamp = timestamp
        self.author_id = author_id

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
    niokrQuality_active = db.Column(db.Boolean)
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
    plant_Construction = db.Column(db.Float)

    # Накладные расходы
    costOverheads = db.Column(db.Integer)
    amountOverheads = db.Column(db.Integer)
    plant_Overheads = db.Column(db.Float)
    # Расходы на демонтаж
    costDismantling = db.Column(db.Integer)
    amountDismantling = db.Column(db.Integer)
    plant_Destruction = db.Column(db.Float)
    # Бюджет команд
    teamBudget = db.Column(db.Integer)

    # Начальная с/с
    startSS1 = db.Column(db.Integer)
    startSS2 = db.Column(db.Integer)
    prime_cost_start = db.Column(db.Float)

    # Начальные вложения в с/с
    startAttachmentsSS1 = db.Column(db.Integer)
    startAttachmentsSS2 = db.Column(db.Integer)
    prime_cost_base = db.Column(db.Float)

    # Начальные вложения в качество
    startAttachmentsQuality1 = db.Column(db.Integer)
    startAttachmentsQuality2 = db.Column(db.Integer)
    quality_cost_base = db.Column(db.Float)

    # Степень в формуле с/с
    exponentSS1 = db.Column(db.Integer)
    exponentSS2 = db.Column(db.Integer)
    prime_cost_coef = db.Column(db.Float)

    # Степень в формуле качества
    exponentQuality1 = db.Column(db.Integer)
    exponentQuality2 = db.Column(db.Integer)
    quality_cost_coef = db.Column(db.Float)

    # Основание в формуле цены
    baseFormulaCost1 = db.Column(db.Integer)
    baseFormulaCost2 = db.Column(db.Integer)
    price_coef = db.Column(db.Float)

    @staticmethod
    def create_default():
        game = Games()
        game.plant_Construction = 1.0
        game.plant_Overheads = 0.2
        game.plant_Destruction = 0.333333
        game.prime_cost_start = 4.0
        game.prime_cost_base = 33.3333
        game.quality_cost_base = 33.333
        game.prime_cost_coef = 2.0
        game.quality_cost_coef = 2.0
        game.sizeNA = 100
        game.price_coef = 2
        game.cost_min = 3
        return game

    @staticmethod
    def create(form):
        try:
            game = Games(title=form['name'], team_number=form['team-number'], period_number=form['period-number'],

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
            if 'time-start' in form:
                isFirstStart = True
                game.time_start = form['time-start']
            else:
                isFirstStart = False
                game.time_start = datetime.now().time()

            if 'time-duration' in form:
                isOversStart = True
                game.time_duration = form['time-duration']
            else:
                isOversStart = False
                game.time_duration = "00:15"
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

            # Расчет базовых параметоров
            game.prime_cost_start = int(game.startSS1) / int(game.startSS2)
            game.prime_cost_base = int(game.startAttachmentsSS1) / int(game.startAttachmentsSS2)
            game.quality_cost_base = int(game.startAttachmentsQuality1) / int(game.startAttachmentsQuality2)
            game.prime_cost_coef = int(game.exponentSS1) / int(game.exponentSS2)
            game.quality_cost_coef = int(game.exponentQuality1) / int(game.exponentQuality2)
            game.price_coef = int(game.baseFormulaCost1) / int(game.baseFormulaCost2)
            game.plant_Construction = int(game.costFactory) / int(game.amountFactory)
            game.plant_Overheads = int(game.costOverheads) / int(game.amountOverheads)
            game.plant_Destruction = int(game.costDismantling) / int(game.amountDismantling)

            db.session.add(game)
            db.session.commit()
            for i in range(1, int(game.team_number)+1):
                gamer = User(game_id=game.id)
                gamer.generate(i)
                db.session.add(gamer)

            delta = timedelta(hours=game.time_duration.hour,
                              minutes=game.time_duration.minute,
                              microseconds=game.time_duration.microsecond)
            end_time = game.time_start
            for i in range(1, int(game.period_number) + 1):
                period = Period(game_id=game.id)
                if i == 1:
                    period.generate(i, start_time=end_time, period_time=delta, isActive=isFirstStart)
                else:
                    period.generate(i, start_time=end_time, period_time=delta, isActive=isOversStart)
                end_time = period.period_end
                db.session.add(period)

            db.session.commit()

            users = User.query.filter_by(game_id=game.id).all()

            periods = Period.query.filter_by(game_id=game.id, period_number=1).first()

            for user in users:
                solution = Solutions.set_default(period_id=periods.id, game=game, gamer_id=user.id)
                solution.count_personal_params(game)
                db.session.add(solution)

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
    isActive = db.Column(db.Boolean)


    def generate(self, period_number, start_time, period_time, isActive=False):
        self.period_number = period_number
        self.period_start = start_time
        self.period_end = (datetime.combine(datetime.now().date(), start_time) + period_time).time()
        self.period_duration = period_time
        self.isActive = isActive

    @staticmethod
    def check_period(period_id):
        current_time = datetime.now().time()
        period = Period.query.filter_by(id=period_id).first()
        if current_time >= period.period_start and current_time <= period.period_end:
            return True
        return False

    def check_period(self):
        current_time = datetime.now().time()
        if current_time >= self.period_start and current_time <= self.period_end:
            return True
        return False

    @staticmethod
    def getActivePeriod(game_id):
        current_time = datetime.now().time()
        periods = Period.query.filter_by(game_id=game_id).order_by(Period.period_number)
        if periods[0].period_start > current_time:
            return {'succeed': False,
                    'message': 'Период начнется в',
                    'time': periods[0].period_start.strftime('%H:%M:%S')}
        else:
            for period in periods:
                if current_time >= period.period_start and current_time <= period.period_end and period.isActive:
                    return {'succeed': True, 'data': period}
        return {'succeed': False,
                'message': 'Игра завершена в',
                'time':  period.period_end.strftime('%H:%M:%S')}

    @staticmethod
    def getPreviousPeriod(period_id):
        pass


    def isFinished(self):
        current_time = datetime.now().time()
        if current_time >= self.period_end:
            return True
        return False

class Solutions(db.Model):
    __tablename__ = 'solutions'
    id = db.Column(db.Integer, primary_key=True)
    period_id = db.Column(db.Integer, db.ForeignKey('periods.id'))
    gamer_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    # Исходные данные
    cost = db.Column(db.Integer)
    niokrSS = db.Column(db.Integer)
    niokrQuality = db.Column(db.Integer)
    NAFactory = db.Column(db.Integer)
    EuropeFactory = db.Column(db.Integer)
    AsiaFactory = db.Column(db.Integer)
    NAPromotion = db.Column(db.Integer)
    EuropePromotion = db.Column(db.Integer)
    AsiaPromotion = db.Column(db.Integer)
    # Расчетные параметры
    # Расходы
    Budget = db.Column(db.Integer)
    # Спрос (Считается после принятия решения ВСЕМИ игроками)
    Demand_NA = db.Column(db.Integer)
    Demand_Europa = db.Column(db.Integer)
    Demand_Asia = db.Column(db.Integer)

    mult_Demand_NA = db.Column(db.Float)
    mult_Demand_Europa = db.Column(db.Float)
    mult_Demand_Asia = db.Column(db.Float)

    mult_Price = db.Column(db.Float)
    mult_Quality = db.Column(db.Float)

    Quality_Cost_Acc = db.Column(db.Integer)
    Prime_Cost_Acc = db.Column(db.Integer)

    # Объем продаж
    Sales_NA = db.Column(db.Integer)
    Sales_Europa = db.Column(db.Integer)
    Sales_Asia = db.Column(db.Integer)
    Sales = db.Column(db.Float)
    # Себестоимость продукции
    Prime_cost = db.Column(db.Float)
    # Прибыль в периоде
    Profit = db.Column(db.Float)
    Acc_Profit = db.Column(db.Float)

    @staticmethod
    def set_default(period_id, game, gamer_id):
        solution = Solutions()
        solution.gamer_id = gamer_id
        solution.period_id = period_id
        solution.cost = game.cost_default
        solution.niokrSS = game.niokrSS_default
        solution.niokrQuality = game.niokrQuality_default
        solution.NAFactory = game.NAFactory_default
        solution.EuropeFactory = game.EuropeFactory_default
        solution.AsiaFactory = game.AsiaFactory_default
        solution.NAPromotion = game.NAPromotion_default
        solution.EuropePromotion = game.EuropePromotion_default
        solution.AsiaPromotion = game.AsiaPromotion_default
        solution.Acc_Profit = 0
        return solution

    @staticmethod
    def set_previous(period_id, previous_solution):
        solution = Solutions()
        solution.gamer_id = previous_solution.gamer_id
        solution.period_id = period_id
        solution.cost = previous_solution.cost
        solution.niokrSS = previous_solution.niokrSS
        solution.niokrQuality = previous_solution.niokrQuality
        solution.NAFactory = previous_solution.NAFactory
        solution.EuropeFactory = previous_solution.EuropeFactory
        solution.AsiaFactory = previous_solution.AsiaFactory
        solution.NAPromotion = previous_solution.NAPromotion
        solution.EuropePromotion = previous_solution.EuropePromotion
        solution.AsiaPromotion = previous_solution.AsiaPromotion
        solution.Acc_Profit = previous_solution.Acc_Profit
        return solution

    def count_personal_params(self, game, isDemo = False):
        self.Quality_Cost_Acc = int(game.quality_cost_base)
        self.Prime_Cost_Acc = int(game.prime_cost_base)

        if isDemo:
            self.Quality_Cost_Acc += int(self.niokrQuality)
            self.Prime_Cost_Acc += int(self.niokrSS)
        else:
            for solution in Solutions.query.filter_by(gamer_id=self.gamer_id):
                self.Quality_Cost_Acc += int(solution.niokrQuality)
                self.Prime_Cost_Acc += int(solution.niokrSS)

        self.mult_Price = 1 / (int(game.price_coef) ** (int(self.cost) - int(game.cost_min)))
        self.mult_Quality = (self.Prime_Cost_Acc / int(game.quality_cost_base)) ** (1 / int(game.quality_cost_coef))

        self.Prime_cost = game.prime_cost_start + 1 - (self.Prime_Cost_Acc / game.prime_cost_base) ** (
        1 / game.prime_cost_coef)

        self.mult_Demand_NA = self.mult_Quality * self.mult_Price * float(self.NAPromotion)
        if not isDemo:
            self.mult_Demand_Europa = self.mult_Quality * self.mult_Price * float(self.EuropePromotion)
            self.mult_Demand_Asia = self.mult_Quality * self.mult_Price * float(self.AsiaPromotion)

    def update_solution(self, form):
        if 'budget' in form:
            self.Budget = form['budget']

        if 'cost' in form:
            self.cost = form['cost']

        if 'niokrSS' in form:
            self.niokrSS = form['niokrSS']

        if 'niokrQuality' in form:
            self.niokrQuality = form['niokrQuality']

        if 'NAFactory' in form:
            self.NAFactory = form['NAFactory']

        if 'EuropeFactory' in form:
            self.EuropeFactory = form['EuropeFactory']

        if 'AsiaFactory' in form:
            self.AsiaFactory = form['AsiaFactory']

        if 'NAPromotion' in form:
            self.NAPromotion = form['NAPromotion']

        if 'EuropePromotion' in form:
            self.EuropePromotion = form['EuropePromotion']

        if 'AsiaPromotion' in form:
            self.AsiaPromotion = form['AsiaPromotion']



    @staticmethod
    def getPreviousSolutions(current_period_id):
        current_period = Period.query.filter_by(id=current_period_id).first()
        previous_period = Period.query.filter_by(game_id=current_period.game_id, period_number=current_period.period_number-1).first()
        return Solutions.query.filter_by(period_id=previous_period.id).all()

    @staticmethod
    def getPreviousSolution(current_period, user_id):
        if current_period.period_number != 1:
            previous_period = Period.query.filter_by(game_id=current_period.game_id,
                                                     period_number=current_period.period_number - 1).first()
            return Solutions.query.filter_by(period_id=previous_period.id, gamer_id=user_id).first()
        else:
            return None


    @staticmethod
    def getSolutions(period):
        return Solutions.query.filter_by(period_id=period.id).all()
