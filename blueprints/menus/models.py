from blueprints.users.models import db
from sqlalchemy.sql import func
from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base


# 中間テーブル
class MenuMaterialMenu(db.Model):
    __tablename__ = 'menu_material_menus'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), comment='ユーザーID', nullable=False)
    fixed_menu_material_id = db.Column(db.Integer, db.ForeignKey('fixed_menu_materials.id'), comment='メニュー材料ID',
                                       nullable=False)
    menu_id = db.Column(db.Integer, db.ForeignKey('menus.id'), comment='メニューID', nullable=False)
    memo = db.Column(db.String(128), comment='メモ')
    quantity = db.Column(db.Integer, comment='個数', nullable=False, default=1)

    fixed_menu_materials = relationship("FixedMenuMaterial", back_populates="menu_material_menus")
    # menu_materials = relationship("MenuMaterial", back_populates="menu_material_menus")
    menus = relationship("Menu", back_populates="menu_material_menus")

    __table_args__ = (
        UniqueConstraint('fixed_menu_material_id', 'menu_id', 'user_id', name='uix_menu_material_id_menu_id_user_id'),)


class FixedMenuMaterial(db.Model):
    __tablename__ = 'fixed_menu_materials'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    category_id = db.Column(db.Integer, db.ForeignKey('fixed_categories.id'), comment='カテゴリーID', nullable=False)
    name = db.Column(db.String(128), comment='献立材料名', nullable=False, unique=True)

    menu_material_menus = relationship("MenuMaterialMenu", back_populates="fixed_menu_materials")


# class MenuMaterial(db.Model):
#     __tablename__ = 'menu_materials'
#
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('users.id'), comment='ユーザーID', nullable=False)
#     category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), comment='カテゴリーID', nullable=False)
#     name = db.Column(db.String(128), comment='献立材料名', nullable=False)
#
#     menu_material_menus = relationship("MenuMaterialMenu", back_populates="menu_materials")
#
#     __table_args__ = (UniqueConstraint('user_id', 'name', name='uix_user_id_menu_material_name'),)


class Menu(db.Model):
    __tablename__ = 'menus'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), comment='ユーザーID', nullable=False)
    name = db.Column(db.String(128), comment='メニュー名', nullable=False)

    menu_material_menus = relationship("MenuMaterialMenu", back_populates="menus")

    __table_args__ = (UniqueConstraint('user_id', 'name', name='uix_user_id_menu_name'),)
