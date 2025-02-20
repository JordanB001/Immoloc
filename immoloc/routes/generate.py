from flask import Blueprint, jsonify, request

from ..model import model, client
from ..remove_star import remove_star

bp = Blueprint("generate", __name__)

@bp.route("/generate", methods=["POST"])
def generate():
    try:
        data: dict = request.get_json()
        
        if data["real_estate_ad"]:
            if isinstance(data["real_estate_ad"], str):
                real_estate_ad: str = data["real_estate_ad"]
            else:
                return "Data error: must be a string", 400
        else:
            return "Data missing: real_estate_ad", 400
    except Exception as e:
        return f"Data error or data missing: {e}", 400
    
    try:
        chat_response = client.chat.complete(
            model= model,
            messages = [
                {
                    "role": "user",
                    "content": f"Write a fluid and attractive real estate ad. if information is missing, then it will indicate at the end of the ad suggestions for information to provide to improve the ad. In French. Here is the announcement: {real_estate_ad}."
                }
            ]
        )
    except Exception as e:
        return f"{e}", 400
    
    
    
    return jsonify({"real_estate_ad": remove_star(chat_response.choices[0].message.content)}), 200
