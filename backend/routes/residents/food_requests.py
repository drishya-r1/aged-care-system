from flask import Blueprint, request, jsonify
from backend.database import excel_manager

food_bp = Blueprint('food', __name__)

@food_bp.route('/api/foodrequest', methods=['POST'])
def add_food_request():
    # Expects JSON with keys matching meal_requests.xlsx columns
    data = request.get_json()
    if not data:
        return jsonify({'success': False, 'message': 'No data provided'}), 400

    # Optionally, validate required fields here
    required = ['request_id', 'resident_id', 'meal_date', 'meal_type', 'menu_item_id', 'special_notes', 'status']
    if not all(k in data for k in required):
        return jsonify({'success': False, 'message': 'Missing required fields'}), 400

    excel_manager.add_record('meal_requests.xlsx', data)
    return jsonify({'success': True, 'message': 'Food request added'})

@food_bp.route('/api/menu/<int:resident_id>', methods=['GET'])
def get_menu_for_resident(resident_id):
    # Get resident's dietary restrictions
    restrictions = excel_manager.get_records_by_column('dietary_restrictions.xlsx', 'resident_id', resident_id)
    restriction_types = set(r['restriction_type'].lower() for r in restrictions)
    restriction_descs = set(r['description'].lower() for r in restrictions)
    print("restriction_types:", restriction_types)
    print("restriction_descs:", restriction_descs)
    # Get all menu items
    menu_items = excel_manager.read_all_rows('menu_items.xlsx')
    filtered_menu = []

    for item in menu_items:
        print("Processing menu item:", item)
        allergens_raw = item.get('allergens')
        allergens_str = allergens_raw if isinstance(allergens_raw, str) else ''
        allergens = set(allergens_str.lower().replace(' ', '').split(',')) if allergens_str else set()

        suitable_for_raw = item.get('suitable_for')
        suitable_for_str = suitable_for_raw if isinstance(suitable_for_raw, str) else ''
        suitable_for = set(suitable_for_str.lower().replace(' ', '').split(',')) if suitable_for_str else set()

        # Exclude menu items with allergens matching any restriction description
        if allergens & restriction_descs:
            continue
        # Exclude menu items not suitable for restriction types (e.g., vegetarian, vegan)
        if restriction_types and not suitable_for.issuperset(restriction_types):
            continue

        filtered_menu.append(item)
        print("Filtered menu items:", filtered_menu)
    return jsonify({'menu': filtered_menu})

@food_bp.route('/api/ondemand_food_menu', methods=['GET'])
def get_ondemand_food_menu():
    items = excel_manager.read_all_food_items()
    return jsonify({'menu': items})

@food_bp.route('/api/request_ondemand_food', methods=['POST'])
def request_ondemand_food():
    data = request.get_json()
    required = ['alert_id', 'resident_id', 'food_item_id', 'food_item_name', 'timestamp', 'details', 'status']
    if not all(k in data for k in required):
        return jsonify({'success': False, 'message': 'Missing required fields'}), 400
    excel_manager.add_food_alert(data)
    return jsonify({'success': True, 'message': 'Food request submitted'})
