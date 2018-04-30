from bson import ObjectId
from flask import Flask, render_template
from flask_login import LoginManager, login_required
from flask_mongoengine import MongoEngine

from flask_bootstrap import Bootstrap

from app.api import api as api_blueprint
from app.auth import auth as auth_blueprint
from app.models import User

app = Flask(__name__,
            static_folder="../dash/static",
            template_folder="../dash")

app.config.from_object('app.config.DevelopmentConfig')

db = MongoEngine(app)

login_manager = LoginManager()
login_manager.init_app(app)

login_manager.login_view = "auth.login"
login_manager.login_message = u"Bonvolu ensaluti por uzi tiun paĝon."
login_manager.login_message_category = "info"

Bootstrap(app)

app.register_blueprint(auth_blueprint, url_prefix='/auth')
app.register_blueprint(api_blueprint, url_prefix='/api')


@login_manager.user_loader
def load_user(user_id):
    return User.objects(id=ObjectId(user_id)).first()


@app.route("/user")
@login_required
def user():
    return render_template('user.html', active="user")


@app.route('/')
@login_required
def index():
    return render_template('index.html', active="index")
