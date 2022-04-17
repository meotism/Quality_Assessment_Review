from flask import Blueprint
from api.review.review import review_blueprint

api_blueprint = Blueprint('api_blueprint', __name__)
api_blueprint.register_blueprint(review_blueprint, url_prefix='/review')
