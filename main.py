# main.py
from flask import Flask, jsonify, request

app = Flask(__name__)

# Store items in memory (simple in-memory database)
items = []
item_id_counter = 1

@app.route('/', methods=['GET'])
def home():
    """Home endpoint"""
    return jsonify({
        "message": "Welcome to the Flask API",
        "endpoints": {
            "GET /": "Home page",
            "GET /items": "Get all items",
            "POST /items": "Create a new item (JSON: {name, description})",
            "GET /items/<id>": "Get item by ID",
            "PUT /items/<id>": "Update item by ID (JSON: {name, description})",
            "DELETE /items/<id>": "Delete item by ID"
        }
    })

@app.route('/items', methods=['GET'])
def get_items():
    """Get all items"""
    return jsonify({"items": items})

@app.route('/items', methods=['POST'])
def create_item():
    """Create a new item"""
    global item_id_counter
    
    data = request.get_json()
    if not data or 'name' not in data:
        return jsonify({"error": "Name is required"}), 400
    
    item = {
        "id": item_id_counter,
        "name": data['name'],
        "description": data.get('description', '')
    }
    items.append(item)
    item_id_counter += 1
    
    return jsonify(item), 201

@app.route('/items/<int:item_id>', methods=['GET'])
def get_item(item_id):
    """Get item by ID"""
    item = next((item for item in items if item['id'] == item_id), None)
    if item is None:
        return jsonify({"error": "Item not found"}), 404
    return jsonify(item)

@app.route('/items/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    """Update item by ID"""
    item = next((item for item in items if item['id'] == item_id), None)
    if item is None:
        return jsonify({"error": "Item not found"}), 404
    
    data = request.get_json()
    if data:
        if 'name' in data:
            item['name'] = data['name']
        if 'description' in data:
            item['description'] = data['description']
    
    return jsonify(item)

@app.route('/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    """Delete item by ID"""
    global items
    item = next((item for item in items if item['id'] == item_id), None)
    if item is None:
        return jsonify({"error": "Item not found"}), 404
    
    items = [item for item in items if item['id'] != item_id]
    return jsonify({"message": "Item deleted successfully"})

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
