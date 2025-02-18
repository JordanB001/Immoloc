from flask import Blueprint, request

from ..model import model, client


bp = Blueprint("analyzer", __name__)

@bp.route("/analyzer", methods=["POST"])
def analyzer():
    
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
        chat_reponse = client.chat.complete(
            model= model,
            messages = [
                {
                    "role": "user",
                    "content": f"Analysis of real estate advertisements, Your goal is to give a critical opinion on this real estate ad. In French. (If in the ad there is no price (rent per month), surface area in m² or location, then you just have to say: 'PAS ASSEZ DE CRITÈRES'), . Here is the announcement: {real_estate_ad}"
                }
            ]
        )
    except Exception as e:
        return f"{e}", 400
    
    
    
    
    
    return chat_reponse.choices[0].message.content, 200
