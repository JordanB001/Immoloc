from flask import Blueprint, request


bp = Blueprint("generate", __name__)

@bp.route("/generate", methods=["POST"])
def generate():
    return 200
