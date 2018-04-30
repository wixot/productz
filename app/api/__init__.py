from flask import Blueprint

api = Blueprint('api', __name__)

from app.api import user
from app.api import apps
from app.api import networks
from app.api import credentials
from app.api import inappproducts
from app.api import data
from app.api import order
from app.api import media