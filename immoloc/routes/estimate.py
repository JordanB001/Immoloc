
import re
from flask import Blueprint, json, jsonify, request

from ..model import model, client
from ..verify_parameters import verify_parameters

bp = Blueprint("estimate", __name__)


@bp.route("/estimate", methods=["POST"])
def estimate():
    try:
        data: dict = request.get_json()
        
        if "real_estate_ad" in data:
            if isinstance(data["real_estate_ad"], str):
                real_estate_ad: str = data["real_estate_ad"]
            else:
                return jsonify({"error": "Data error: must be a string"}), 400
        else:
            return jsonify({"error": "Data missing: real_estate_ad"}), 400
    except Exception as e:
        return jsonify({"error": f"Data error or data missing: {e}"}), 400
    
    verify_parameters(real_estate_ad, area=True, type_of_property=True)
    
    try:
        chat_response = client.chat.complete(
            model= model,
            messages = [
                {
                    "role": "user",
                    "content": f"Estimate a price range for a property. In format JSON : 'average_price' : add price here, 'min_range' : add min range prince here, 'max_range' :  add max range price here.  In French. Here is the announcement: {real_estate_ad},  Only If there is no place/location then display 'Entrer la localisation'."
                }
            ]
        )
    except Exception as e:
        return f"{e}", 400
    
    if "Entrer la localisation" in chat_response.choices[0].message.content:
        return jsonify({"error": "Data missing: location / not precise enough"}), 400

    try:
        match = re.search(r'\`\`json\s*([\s\S]*?)\s*\`\`', chat_response.choices[0].message.content)
        if match:
            json_str = match.group(1)
            data = json.loads(json_str) 
    except Exception as e:
        return f"Error parsing JSON response: {e}", 400
    
    return data, 200