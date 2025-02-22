from flask import Blueprint, request, jsonify

from ..model import model, client
from ..verify_parameters import verify_parameters
from ..remove_star import remove_star


bp = Blueprint("analyzer", __name__)

@bp.route("/analyzer", methods=["POST"])
def analyzer():
    """
    Analyzes a real estate advertisement and provides a critical opinion in French.
    This function expects a JSON payload with a key "real_estate_ad" containing the advertisement text.
    It uses an external chat model to generate a critical opinion on the advertisement.
    Returns:
        Response: A JSON response containing the critical opinion or an error message.
    Request JSON format:
        "real_estate_ad": "string"
    Responses:
        200 OK: 
            "real_estate_ad": "string"  # The critical opinion generated by the chat model.
        400 Bad Request:
            "error": "string"  # Error message indicating what went wrong.
    """
   
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
    
    verify_result: list = verify_parameters(real_estate_ad, area=True, price=True, type_of_property=True)
    if not verify_result[0]:
        return jsonify({"error": verify_result[1]}), 400
        
    try:
        chat_response = client.chat.complete(
            model=model,
            messages=[
                {
                    "role": "user",
                    "content": f"Analysis of real estate advertisements, Your goal is to give a critical opinion on this real estate ad and concise, 5 sentences max. In French. Here is the announcement: {real_estate_ad}. Only If there is no place/location then display 'Entrer la localisation' and don't comment this."
                }
            ]
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 400

    print(chat_response.choices[0].message.content)
    if "Entrer la localisation" in chat_response.choices[0].message.content:
        return jsonify({"error": "Data missing: location / not precise enough"}), 400
    
    return jsonify({"real_estate_ad": remove_star(chat_response.choices[0].message.content)}), 200
