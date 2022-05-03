from flask import Blueprint
from api.data.data_controller import data_blueprint
from api.review.review import review_blueprint
from api.initialize.index import init_blueprint

api_blueprint = Blueprint('api_blueprint', __name__)

api_blueprint.register_blueprint(data_blueprint, url_prefix='/data')
api_blueprint.register_blueprint(review_blueprint, url_prefix='/review')
api_blueprint.register_blueprint(init_blueprint, url_prefix='/initialize')
