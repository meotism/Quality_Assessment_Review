from flask import Blueprint, request, redirect
from api.review.handle import *
init_blueprint = Blueprint('init_blueprint', __name__)


@init_blueprint.route('/', methods=['GET'])
def index():
    data = DBdevideGroup()
    return {"data": data}, 200


@init_blueprint.route('/', methods=['POST'])
def create():
    data = createlabel()
    return {"data": data}, 200
