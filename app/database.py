from . import db, loginManager
from flask_login import UserMixin
from datetime import datetime
from flask import current_app, request, url_for
from werkzeug.security import generate_password_hash, check_password_hash


@loginManager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role')

    def __repr__(self):
        return '<Role %r>' % self.name



class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    password_hash = db.Column(db.String(128))

    @property
    def password(self):
        raise AttributeError('Err')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password, salt_length=2)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User %r>' % self.username



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
    numberOfCompanies = db.Column(db.Integer)
    # Количество периодов
    numberOfPeriod = db.Column(db.Integer)
    # Начало и время периода
    game_start = db.Column(db.DateTime)
    period_time = db.Column(db.Time)
    # Объем Рынков
    # СА
    volume_of_markets_sa = db.Column(db.Integer)
    sa_active = db.Column(db.Boolean)
    # Европа
    volume_of_markets_europe = db.Column(db.Integer)
    europe_active = db.Column(db.Boolean)
    # Азия
    volume_of_markets_asia = db.Column(db.Integer)
    asia_active = db.Column(db.Boolean)

    # Доступные решения
    # Цена
    cost_active = db.Column(db.Integer)
    cost_default = db.Column(db.Integer)
    cost_min = db.Column(db.Integer)
    cost_max = db.Column(db.Integer)
    # НИОКР (с/с)
    niocr_s_s_active = db.Column(db.Integer)
    niocr_s_s_default = db.Column(db.Integer)
    niocr_s_s_min = db.Column(db.Integer)
    niocr_s_s_max = db.Column(db.Integer)
    # НИОКР (качество)
    niocr_quality_active = db.Column(db.Integer)
    niocr_quality_default = db.Column(db.Integer)
    niocr_quality_min = db.Column(db.Integer)
    niocr_quality_max = db.Column(db.Integer)

    #Заводы
    # СА
    sa_factory_active = db.Column(db.Boolean)
    sa_factory_default = db.Column(db.Integer)
    sa_factory_min = db.Column(db.Integer)
    sa_factory_max = db.Column(db.Integer)
    # Европа
    europe_factory_active = db.Column(db.Boolean)
    europe_factory_default = db.Column(db.Integer)
    europe_factory_min = db.Column(db.Integer)
    europe_factory_max = db.Column(db.Integer)
    # Азия
    asia_factory_active = db.Column(db.Boolean)
    asia_factory_default = db.Column(db.Integer)
    asia_factory_min = db.Column(db.Integer)
    asia_factory_max = db.Column(db.Integer)

    # Продвижение
    # СА
    sa_promotion_active = db.Column(db.Boolean)
    sa_promotion_default = db.Column(db.Integer)
    sa_promotion_min = db.Column(db.Integer)
    sa_promotion_max = db.Column(db.Integer)
    # Европа
    europe_promotion_active = db.Column(db.Boolean)
    europa_promotion_default = db.Column(db.Integer)
    europe_promotion_min = db.Column(db.Integer)
    europe_promotion_max = db.Column(db.Integer)
    # Азия
    asia_promotion_active = db.Column(db.Boolean)
    asia_promotion_default = db.Column(db.Integer)
    asia_promotion_min = db.Column(db.Integer)
    asia_promotion_max = db.Column(db.Integer)

    # Базовые параметры
    # Строительство завода
    buld_factory_cost = db.Column(db.Integer)
    buld_factory_volume = db.Column(db.Integer)

    # Накладные расходы
    overheads_cost = db.Column(db.Integer)
    overheads_volume = db.Column(db.Integer)

    # Расходы на демонтаж
    dismantling_costs = db.Column(db.Integer)
    dismantling_volume = db.Column(db.Integer)

    # Бюджет команд
    team_budget = db.Column(db.Integer)

    # Начальная с/с
    started_s_s_first = db.Column(db.Integer)
    started_s_s_second = db.Column(db.Integer)

    # Начальные вложения в с/с
    started_attachments_s_s_first = db.Column(db.Integer)
    started_attachments_s_s_second = db.Column(db.Integer)

    # Начальные вложения в качество
    started_attachments_quality_first = db.Column(db.Integer)
    started_attachments_quality_second = db.Column(db.Integer)

    # Степень в формуле с/с
    formula_degree_s_s_first = db.Column(db.Integer)
    formula_degree_s_s_second = db.Column(db.Integer)

    # Степень в формуле качества
    formula_degree_quality_first = db.Column(db.Integer)
    formula_degree_quality_second = db.Column(db.Integer)

    # Основание в формуле цены
    basis_price_formula_first = db.Column(db.Integer)
    basis_price_formula_second = db.Column(db.Integer)





