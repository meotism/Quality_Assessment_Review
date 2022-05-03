from flask import Blueprint, request, jsonify
from api.review.handle import *

review_blueprint = Blueprint('review_blueprint', __name__)


@review_blueprint.route('/', methods=['GET'])
def runAgain():
    data = devideGroup()
    return {"data": data}, 200


@review_blueprint.route('/', methods=['POST'])
def create():
    data = DBcreatelabel()
    return {"data": data}, 200
