from flask import Blueprint

main = Blueprint('main', __name__)

from app.main.controller import error_controller,user_controller, message_controller, kafka_controller


