from blueprints.users.models import db
from sqlalchemy.sql import func
from sqlalchemy import UniqueConstraint, Date


class WastedMaterial(db.Model):
    __tablename__ = 'wasted_materials'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), comment='ユーザーID', nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('fixed_categories.id'), comment='カテゴリーID', nullable=False)
    material_id = db.Column(db.Integer, db.ForeignKey('fixed_menu_materials.id'), comment='材料ID', nullable=False)
    memo = db.Column(db.String(128), comment='メモ')
    quantity = db.Column(db.Integer, comment='数量', nullable=False)
    purchase_date = db.Column(db.Date, comment='購入日', nullable=False)
    expiration_date = db.Column(db.Date, comment='賞味期限', nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now(), comment='作成日')
