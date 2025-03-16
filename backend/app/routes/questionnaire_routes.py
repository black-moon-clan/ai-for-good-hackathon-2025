from flask import Blueprint, request, jsonify
from datetime import datetime
import uuid

questionnaire_bp = Blueprint('questionnaire', __name__)

# In-memory storage for this example
questionnaires = []

@questionnaire_bp.route('/', methods=['POST'])
def create_questionnaire():
    try:
        data = request.get_json()
        data['id'] = str(uuid.uuid4())  # Generate UUID
        data['created_at'] = datetime.now().isoformat()
        questionnaires.append(data)
        return jsonify(data), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@questionnaire_bp.route('/', methods=['GET'])
def get_questionnaires():
    return jsonify(questionnaires), 200

@questionnaire_bp.route('/<questionnaire_id>', methods=['GET'])
def get_questionnaire(questionnaire_id):
    questionnaire = next((q for q in questionnaires if q['id'] == questionnaire_id), None)
    if questionnaire:
        return jsonify(questionnaire), 200
    return jsonify({"error": "Questionnaire not found"}), 404

@questionnaire_bp.route('/<questionnaire_id>', methods=['PUT'])
def update_questionnaire(questionnaire_id):
    try:
        data = request.get_json()
        index = next((i for i, q in enumerate(questionnaires) if q['id'] == questionnaire_id), None)
        if index is not None:
            data['id'] = questionnaire_id
            data['created_at'] = questionnaires[index]['created_at']
            questionnaires[index] = data
            return jsonify(data), 200
        return jsonify({"error": "Questionnaire not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@questionnaire_bp.route('/<questionnaire_id>', methods=['DELETE'])
def delete_questionnaire(questionnaire_id):
    global questionnaires
    initial_length = len(questionnaires)
    questionnaires = [q for q in questionnaires if q['id'] != questionnaire_id]
    if len(questionnaires) < initial_length:
        return jsonify({"message": "Questionnaire deleted successfully"}), 200
    return jsonify({"error": "Questionnaire not found"}), 404

@questionnaire_bp.route('/<questionnaire_id>/status', methods=['PUT'])
def update_status(questionnaire_id):
    try:
        data = request.get_json()
        new_status = data.get('status')
        index = next((i for i, q in enumerate(questionnaires) if q['id'] == questionnaire_id), None)
        
        if index is not None:
            questionnaires[index]['status'] = new_status
            return jsonify(questionnaires[index]), 200
        return jsonify({"error": "Questionnaire not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 400 