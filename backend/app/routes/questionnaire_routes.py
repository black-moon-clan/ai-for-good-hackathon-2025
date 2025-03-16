from flask import Blueprint, request, jsonify
from datetime import datetime

questionnaire_bp = Blueprint('questionnaire', __name__)

# In-memory storage for this example
questionnaires = []

@questionnaire_bp.route('/', methods=['POST'])
def create_questionnaire():
    try:
        data = request.get_json()
        data['created_at'] = datetime.now().isoformat()
        questionnaires.append(data)
        return jsonify({"message": "Questionnaire created successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@questionnaire_bp.route('/', methods=['GET'])
def get_questionnaires():
    return jsonify(questionnaires), 200 