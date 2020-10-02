from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, LoginManager, login_required, login_user, current_user
from os import environ


app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecret'
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DATABASE_URL') or 'sqlite:///pokemons.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db= SQLAlchemy(app)

# create login_manager here:
login_manager = LoginManager()
login.login_view = 'login'
# initialize login_manager here:
login_manager.init_app(app)

class Users(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), index=True, unique=True)
    email = db.Column(db.String(100), index=True, unique=True)
    password = db.Column(db.String(100), index=True)
    joined_at_date = db.Column(db.DateTime(), index=True, default=datetime.utcnow)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def set_password(self, password):
        self.password = generate_password_hash(password)

@login_manager.user_loader
def load_user(id):
    return Users.query.get(int(id))


@app.route('/', methods =["GET","POST"])
def index():

    return render_template('index.html')


@app.route('/register', methods =["GET","POST"])
def register():


    return render_template('register.html')


@app.route('/register/add', methods =["GET", "POST"])
def register_add():
    if request.method == "POST":
            user= Users(
                username = request.form.get('username').lower(),
                email = request.form.get('email')
            )
            user.set_password(request.form.get('password'))
            db.session.add(user)
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()
                return redirect(url_for('register_err'))


    return redirect(url_for("login"))


@app.route('/login', methods =["GET","POST"])
def login():
    if request.method == "POST":
        user = Users.query.filter_by(username=request.form['username_log']).first()

        if user and user.check_password(request.form['password_log']) :
            login_user(user)
            return  redirect(url_for('game'))


        return  redirect(url_for('login_err'))


    return render_template('login.html')


@app.route('/game', methods =["GET","POST"])
@login_required
def game():
    return render_template('game.html')


@login_manager.unauthorized_handler
def unauthorized():
    # do stuff
    return "You are not logged in. Click here to get <a href="+ str("/")+">back to Landing Page</a>"


# ERRORS TEMPLATES
@app.route('/login/error', methods =["GET","POST"])
def login_err():
    return render_template('error.html')

@app.route('/register/error', methods =["GET","POST"])
def register_err():
    return render_template('integrityError.html')

@app.route('/test', methods =["GET","POST"])
def test():
    return render_template('test.html')


