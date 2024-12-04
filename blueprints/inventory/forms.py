import re
from wtforms import StringField, IntegerField, DateField, validators, SelectField, HiddenField
from flask_wtf import FlaskForm
from wtforms.fields.numeric import IntegerField
from wtforms.validators import DataRequired, Length, ValidationError
from wtforms_sqlalchemy.fields import QuerySelectField
from .models import FixedCategory, FixedCategory
from ..menus.models import FixedMenuMaterial
from flask_login import current_user
from datetime import date


class CategoryForm(FlaskForm):
    category_name = StringField('名前', validators=[DataRequired(), Length(min=1, max=60)])


def category_choices():
    return FixedCategory.query.all()
    # return Category.query.filter_by(user_id=current_user.id).all()


def sub_category_choices(category_id):
    return FixedMenuMaterial.query.filter_by(category_id=category_id).all()


def get_id_from_category(obj):
    return str(obj.id)


def get_id_from_category(obj):
    return str(obj.id)


class InventoryForm(FlaskForm):
    category_id = QuerySelectField('カテゴリー', query_factory=category_choices, allow_blank=True,
                                   validators=[DataRequired()],
                                   get_label='category_name',
                                   get_pk=get_id_from_category, render_kw={'id': 'category_select'})
    material_id = SelectField('食材', validators=[DataRequired()],
                              render_kw={'id': 'material_select'})
    memo = StringField('メモ', validators=[Length(min=0, max=120)])
    quantity = IntegerField('個数', default=1, validators=[DataRequired()])
    purchase_date = DateField('購入日', default=date.today, validators=[DataRequired()])
    expiration_date = DateField('消費期限', validators=[DataRequired()])
    initial_category_id = HiddenField()
    initial_material_id = HiddenField()


class SearchForm(FlaskForm):
    category = QuerySelectField('カテゴリー', query_factory=category_choices, allow_blank=True,
                                blank_text='カテゴリーを選択', validators=[DataRequired()], get_label='category_name',
                                get_pk='id')
    search_string = StringField('検索文字列', validators=[DataRequired(), Length(min=1, max=120)])
