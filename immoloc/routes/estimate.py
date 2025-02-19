import re
from flask import Blueprint, json, jsonify, request
from ..model import model, client

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
        
    try:
        chat_response = client.chat.complete(
            model= model,
            messages = [
                {
                    "role": "user",
                    "content": f"Calculate a price range for a property. In French. Here is the announcement: {real_estate_ad},  Only If there is no place/location then display 'Entrer la localisation', Only If there is no surface (m2 / m² / m 2) then display 'Entrer la surface du bien', Only If there is no type of property then display 'Entrer le type du bien'"
                }
            ]
        )
    except Exception as e:
        return f"{e}", 400
    
    if "Entrer la localisation" in chat_response.choices[0].message.content:
        return jsonify({"error": "Data missing: location"}), 400
    if "Entrer la surface du bien" in chat_response.choices[0].message.content:
        return jsonify({"error": "Data missing: surface area"}), 400
    if "Entrer le type du bien" in chat_response.choices[0].message.content:
        return jsonify({"error": "Data missing: type of property"}), 400
    
    match = re.search(r'\`\`\`json\s*([\s\S]*?)\s*\`\`\`', chat_response.choices[0].message.content)
    if match:
        json_str = match.group(1)
        data_result = json.loads(json_str)
        print(data)
    
    
    return data_result , 200
    
