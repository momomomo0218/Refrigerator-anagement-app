from blueprints.users.models import db
from sqlalchemy.sql import func
from sqlalchemy import UniqueConstraint


class FixedCategory(db.Model):
    __tablename__ = 'fixed_categories'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    category_name = db.Column(db.String(64), comment='カテゴリー名', nullable=False, unique=True)


# class Category(db.Model):
#     __tablename__ = 'categories'
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('users.id'), comment='ユーザーID', nullable=False)
#     category_name = db.Column(db.String(64), comment='カテゴリー名', nullable=False)
#
#     __table_args__ = (UniqueConstraint('user_id', 'category_name', name='uix_user_id_category_name'),)


class Inventory(db.Model):
    __tablename__ = 'inventory'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='ID')
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), comment='ユーザーID', nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('fixed_categories.id'), comment='カテゴリーID', nullable=False)
    material_id = db.Column(db.Integer, db.ForeignKey('fixed_menu_materials.id'), comment='材料ID', nullable=False)
    memo = db.Column(db.String(128), comment='メモ')
    quantity = db.Column(db.Integer, comment='数量', nullable=False)
    purchase_date = db.Column(db.Date, comment='購入日', nullable=False)
    expiration_date = db.Column(db.Date, comment='賞味期限', nullable=False)

    user = db.relationship('User', backref='inventory')
    category = db.relationship('FixedCategory', backref='inventory')
    material = db.relationship('FixedMenuMaterial', backref='inventory')
