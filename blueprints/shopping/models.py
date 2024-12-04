from blueprints.users.models import db
from sqlalchemy.sql import func
from sqlalchemy import UniqueConstraint, Date


class ShoppingList(db.Model):
    __tablename__ = 'shopping_list'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), comment='ユーザーID', nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('fixed_categories.id'), comment='カテゴリーID', nullable=False)
    material_id = db.Column(db.Integer, db.ForeignKey('fixed_menu_materials.id'), comment='材料ID', nullable=False)
    memo = db.Column(db.String(128), comment='メモ')
    quantity = db.Column(db.Integer, comment='数量', nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now(), comment='作成日')

    __table_args__ = (UniqueConstraint('user_id', 'material_id', name='uix_user_id_material_id'),)
