import re
from wtforms import StringField, PasswordField, BooleanField, validators, HiddenField
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Length, ValidationError


class LoginForm(FlaskForm):
    username = StringField('ユーザー名', [validators.Length(min=4, max=25)], render_kw={"autocomplete": "off"})
    password = PasswordField('パスワード', [validators.DataRequired()], render_kw={"autocomplete": "off"})
    remember_me = BooleanField(label='次回から自動的にログインする')
    next = HiddenField('next')  # この行によって 'next' フィールドが追加されます。


class SignupForm(FlaskForm):
    def validate_password(self, field):
        password = field.data
        if len(password) < 6 or not re.search(r"\d", password) or not re.search(r"[a-zA-Z]", password):
            raise ValidationError('パスワードは6文字以上で、英数字をそれぞれ1文字以上含む必要があります。')

    username = StringField('ユーザー名', validators=[Length(min=4, max=25)])
    password = PasswordField('パスワード', validators=[DataRequired()])
