from flask import Flask, request, jsonify
from utils.qr_generator import generate_qr
from utils.delivery_resolver import detect_delivery_partner
from utils.rzp_linker import create_payment_link
from models.hf_model_loader import generate_caption

app = Flask(__name__)

@app.route('/')
def index():
    return jsonify({"message": "SellXpress Infinity API is running."})

@app.route('/generate_caption', methods=['POST'])
def caption():
    data = request.json
    product_name = data.get("product_name", "")
    language = data.get("language", "en")
    if not product_name:
        return jsonify({"error": "Missing product name"}), 400
    caption = generate_caption(product_name, language)
    return jsonify({"caption": caption})

@app.route('/create_qr', methods=['POST'])
def create_qr():
    data = request.json
    store_url = data.get("store_url", "")
    if not store_url:
        return jsonify({"error": "Missing store_url"}), 400
    qr_path = generate_qr(store_url)
    return jsonify({"qr_code_path": qr_path})

@app.route('/detect_delivery', methods=['POST'])
def detect_delivery():
    data = request.json
    pincode = data.get("pincode")
    city = data.get("city")
    if not city and not pincode:
        return jsonify({"error": "Provide city or pincode"}), 400
    partner = detect_delivery_partner(city=city, pincode=pincode)
    return jsonify({"delivery_partner": partner})

@app.route('/razorpay_link', methods=['POST'])
def razorpay():
    data = request.json
    name = data.get("name")
    amount = data.get("amount")
    if not name or not amount:
        return jsonify({"error": "Name and amount required"}), 400
    link = create_payment_link(name, amount)
    return jsonify({"payment_link": link})

if __name__ == "__main__":
    app.run(debug=True)

