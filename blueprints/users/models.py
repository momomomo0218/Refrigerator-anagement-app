from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager

db = SQLAlchemy()

login_manager = LoginManager()


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, comment='ID')
    username = db.Column(db.String(64), unique=True, comment='ユーザー名', nullable=False)
    password_hash = db.Column(db.String(128), comment='パスワードハッシュ', nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now(), comment='作成日', nullable=False)
    # is_active, is_anonymous など、他の属性が必要であればここに追加します


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
