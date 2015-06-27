from flask.ext.login import login_user , logout_user , current_user , login_required, LoginManager

from server import app
from flask import Blueprint, render_template, abort



pages = []
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'



simple_page = Blueprint('simple_page', __name__,
                        template_folder='templates')
          

from .views import *
from .models import *
