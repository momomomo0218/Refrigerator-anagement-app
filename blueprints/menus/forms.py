import re
from wtforms import StringField, IntegerField, validators, SelectField, HiddenField
from flask_wtf import FlaskForm
# from wtforms.fields.numeric import IntegerField
from wtforms.validators import DataRequired, Length
from wtforms_sqlalchemy.fields import QuerySelectField
from ..inventory.models import FixedCategory, FixedCategory
from flask_login import current_user


def category_choices():
    return FixedCategory.query.all()
    # return Category.query.filter_by(user_id=current_user.id).all()


class EditMenuForm(FlaskForm):
    menu_name = StringField('メニュー名', validators=[DataRequired(), Length(min=1, max=60)])
    category_id = QuerySelectField('カテゴリー', query_factory=category_choices, allow_blank=True,
                                   get_label='category_name', render_kw={'id': 'category_select'})
    menu_material_id = SelectField('材料', validators=[DataRequired()], render_kw={'id': 'material_select'})
    memo = StringField('メモ', validators=[Length(max=128)], render_kw={'id': 'memo'})
    quantity = IntegerField('個数', default=1, validators=[DataRequired()])
