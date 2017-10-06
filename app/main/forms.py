from flask_wtf import FlaskForm as Form
from wtforms import StringField, SubmitField, PasswordField, IntegerField, DateField, TextAreaField, validators
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

class News(Form):
    date = DateField('Дата', [InputRequired()],
                        id="date",
                        _name="date",
                        render_kw={"placeholder": "ГГГГ.ММ.ДД "})
    title = StringField('Заголовок новости', [InputRequired()],
                             id="title",
                             _name="title")
    text = TextAreaField('Текст новости', [InputRequired()],
                             id="text",
                             _name="text")
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