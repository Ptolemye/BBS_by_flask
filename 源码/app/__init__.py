from flask import Flask
import config
app = Flask(__name__)
app.config.from_object(config)
from app import index
from app import login
from app import register
from app import context_processor
from app import logout
from app import admin
from app import publish
from app import profile
from app import post