from flask import (Blueprint, flash, g, redirect, render_template, request, session, url_for)
from app.db.db import get_db
from app.utils import *
from app.function import *


post_bp = Blueprint('post', __name__, url_prefix='/post')