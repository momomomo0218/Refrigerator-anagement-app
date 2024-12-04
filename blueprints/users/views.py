from flask import Blueprint, render_template, request, flash, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from .forms import LoginForm, SignupForm
from .models import User, db
from flask_login import login_user, logout_user, current_user
from urllib.parse import urlparse, urljoin
from werkzeug.routing import BuildError
from passlib.context import CryptContext
from werkzeug.utils import secure_filename

users = Blueprint('users', __name__)


@users.route('/help/')
def help_msg():
    return render_template('users/help.j2')


@users.route('/')
def home():
    if current_user.is_authenticated:
        return redirect(url_for('inventory.index'))
    else:
        return redirect(url_for('users.login'))


@users.route('/signup/', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            username = request.form.get('username')
            password = request.form.get('password')
            if not username or not password:
                flash('Username and password cannot be empty.')
                return redirect(url_for('users.signup'))
            user = User.query.filter_by(username=username).first()
            if user:
                flash(f'{username} はすでに使われています')
                return redirect(url_for('users.signup'))
            new_user = User(username=username, password_hash=generate_password_hash(password, method='pbkdf2:sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_form = LoginForm()
            login_form.username.data = username
            login_form.password.data = ''
            login_form.remember_me.data = False
            return render_template('users/login.j2', form=login_form)
        else:
            return render_template('users/signup.j2', form=form)
    else:
        signup_form = SignupForm()
        return render_template('users/signup.j2', form=signup_form)


@users.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        remember_me = request.form.get('remember_me')
        user = User.query.filter_by(username=username).first()
        if not user or not check_password_hash(user.password_hash, password):
            flash('ログインに失敗しました。ユーザー名とパスワードを確認して、もう一度試してください。')
            return redirect(url_for('users.login'))
        else:
            login_user(user, remember=remember_me)
            next_page = request.form.get('next')
            if next_page:
                netloc = urlparse(next_page).netloc
                if netloc == "" or netloc == request.host:
                    return redirect(next_page)
                else:
                    return 'ERROR'
            else:
                return redirect(url_for('users.home'))
    else:
        if current_user.is_authenticated:
            return redirect(url_for('users.home'))
        else:
            login_form = LoginForm()
            login_form.next.data = request.args.get('next')
            return render_template('users/login.j2', form=login_form)


@users.route('/logout/')
def logout():
    logout_user()
    return redirect(url_for('users.login'))
