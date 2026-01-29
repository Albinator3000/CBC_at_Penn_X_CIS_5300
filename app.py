from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from agent import analyze_brand
import json

app = Flask(__name__, static_folder='static')
CORS(app)

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@app.route('/analyze')
def analyze():
    brand = request.args.get('brand', '').lower()
    if not brand:
        return jsonify({"error": "Brand parameter required"}), 400

    try:
        result = analyze_brand(brand)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/compare')
def compare():
    brands = request.args.get('brands', '').lower().split(',')
    if len(brands) < 2:
        return jsonify({"error": "At least 2 brands required"}), 400

    try:
        results = []
        for brand in brands:
            brand = brand.strip()
            if brand:
                results.append(analyze_brand(brand))
        return jsonify(results)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/brands')
def get_brands():
    with open('data/brands.json', 'r') as f:
        data = json.load(f)
    return jsonify(list(data.keys()))

if __name__ == '__main__':
    app.run(debug=True, port=5000)
