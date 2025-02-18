from flask import Blueprint, request
from ..model import model, client

bp = Blueprint("estimate", __name__)

@bp.route("/estimate", methods=["POST"])
def estimate():
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
                    "content": f"Calculate a price range for a property. If in the ad there is no type of property (house/apartment), surface area in m² or location of the property (City + Postal Code) then you just say 'PAS ASSEZ DE CRITÈRES'. In French. Here is the announcement: {real_estate_ad}"
                }
            ]
        )
    except Exception as e:
        return f"{e}", 400
    
    
    
    return chat_reponse.choices[0].message.content, 200
    
