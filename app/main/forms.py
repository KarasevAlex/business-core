from flask_wtf import FlaskForm as Form
from wtforms import StringField, SubmitField, PasswordField, IntegerField, validators
from wtforms.validators import InputRequired

class Login(Form):
    login = StringField('Логин', [InputRequired()],
                        id="login",
                        _name="login",
                        render_kw={"placeholder": "Ваш логин "})
    password = PasswordField('Пароль', [InputRequired()],
                             id="password",
                             _name="password",
                             render_kw={"placeholder": "Ваш пароль "})
    submit = SubmitField('Войти')


# НУ НАХУЙ ЕЕ ОПИСЫВАТЬ ТАК СОЙДЕТ=)

# class Game(Form):
#     title = StringField('Название', [InputRequired(), ],
#                         id="name",
#                         _name="name",
#                         render_kw={"placeholder": "Название"})
#
#     TeamCount = IntegerField('Количество команд',[InputRequired(), validators.Length(min=2)],
#                              default=2,
#                              id='team-number',
#                              _name='team-number',
#                              render_kw={"placeholder": "Количество команд"})
#     PeriodCount = IntegerField('Количество периодов', [InputRequired(), validators.Length(min=2)],
#                              default=5,
#                              id='period-number',
#                              _name='period-number',
#                              render_kw={"placeholder": "Количество периодов"})