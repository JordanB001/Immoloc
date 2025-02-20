from flask import jsonify

AREA = ["m²", "m2", "m 2"]
PRICE = ["euro", "euros", "€"]
TYPE_OF_PROPERTY = [
    "appartement",
    "maison",
    "maison individuelle",
    "studio",
    "loft",
    "duplex / triplex",
    "villa",
    "château",
    "chateau"
    "manoir",
    "ferme / corps de ferme",
    "maison de ville",
    "pavillon",
    "bungalow",
    "maison de campagne",
    "propriété de prestige",
    "propriete de prestige",
    "immeuble",
    "terrain constructible",
    "terrain agricole",
    "local commercial",
    "vureau",
    "entrepôt",
    "entrepot",
    "hangar",
    "garage / parking",
    "boutique",
    "hôtel particulier",
    "hotel particulier",
    "résidence de services",
    "residence de services",
    "chalet",
    "mobil-home",
    "péniche",
    "peniche"
]

def verify_parameters(text: str, area : bool=False, price: bool=False, type_of_property: bool=False):
    if not isinstance(text, str):
        return jsonify({"error": "Invalid input: text must be a string"}), 400
    if text == "":
        return jsonify({"error": "Invalid input: text cannot be empty"}), 400
    
    msg: str = ""
    
    if area and not any(term in text.lower() for term in AREA):
        msg += "Data missing: surface area."
        #return jsonify({"error": "Data missing: surface area"})
    if price and not any(term in text.lower() for term in PRICE):
        msg += "Data missing: price."
        #return jsonify({"error": "Data missing: price"})
    if type_of_property and not any(term in text.lower() for term in TYPE_OF_PROPERTY):
        msg += "Data missing: type of property."
        #return jsonify({"error": "Data missing: type of property"})
    
    if msg != "":
        return False, msg
    
    return True, msg