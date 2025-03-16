from flask import Flask, Blueprint, request, jsonify
from datetime import datetime
import uuid
from app.services.questionnaire_service import QuestionnaireService
from flask_cors import CORS
from dotenv import load_dotenv

questionnaire_bp = Blueprint('questionnaire', __name__)

# In-memory storage for this example
questionnaires = []

# Load environment variables
load_dotenv()
app = Flask(__name__)
# Configure CORS to allow all origins, methods, and headers
CORS(app, resources={r"/*": {
    "origins": "*",
    "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    "allow_headers": ["Content-Type", "Authorization", "X-Requested-With"]
}}, supports_credentials=True)

@questionnaire_bp.route('/', methods=['POST', 'OPTIONS'])
@questionnaire_bp.route('', methods=['POST', 'OPTIONS'])
def create_questionnaire():
    # Handle OPTIONS request for CORS preflight
    if request.method == 'OPTIONS':
        return '', 204
    
    try:
        data = request.get_json()
        data['id'] = str(uuid.uuid4())  # Generate UUID
        data['created_at'] = datetime.now().isoformat()
        questionnaires.append(data)
        return jsonify(data), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@questionnaire_bp.route('/', methods=['GET', 'OPTIONS'])
@questionnaire_bp.route('', methods=['GET', 'OPTIONS'])
def get_questionnaires():
    # Handle OPTIONS request for CORS preflight
    if request.method == 'OPTIONS':
        return '', 204
    
    return jsonify(questionnaires), 200

@questionnaire_bp.route('/<questionnaire_id>', methods=['GET', 'OPTIONS'])
def get_questionnaire(questionnaire_id):
    # Handle OPTIONS request for CORS preflight
    if request.method == 'OPTIONS':
        return '', 204
    
    questionnaire = next((q for q in questionnaires if q['id'] == questionnaire_id), None)
    if questionnaire:
        return jsonify(questionnaire), 200
    return jsonify({"error": "Questionnaire not found"}), 404

@questionnaire_bp.route('/<questionnaire_id>', methods=['PUT', 'OPTIONS'])
def update_questionnaire(questionnaire_id):
    # Handle OPTIONS request for CORS preflight
    if request.method == 'OPTIONS':
        return '', 204
    
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

@questionnaire_bp.route('/<questionnaire_id>', methods=['DELETE', 'OPTIONS'])
def delete_questionnaire(questionnaire_id):
    # Handle OPTIONS request for CORS preflight
    if request.method == 'OPTIONS':
        return '', 204
    
    global questionnaires
    initial_length = len(questionnaires)
    questionnaires = [q for q in questionnaires if q['id'] != questionnaire_id]
    if len(questionnaires) < initial_length:
        return jsonify({"message": "Questionnaire deleted successfully"}), 200
    return jsonify({"error": "Questionnaire not found"}), 404

@questionnaire_bp.route('/<questionnaire_id>/start', methods=['POST', 'OPTIONS'])
def start_questionnaire(questionnaire_id):
    # Handle OPTIONS request for CORS preflight
    if request.method == 'OPTIONS':
        return '', 204
    
    """
    Start a questionnaire by generating Python code for the flow.
    """
    result = QuestionnaireService.start_questionnaire(questionnaire_id)
    if not result:
        return jsonify({'error': 'Questionnaire not found'}), 404
    return jsonify(result)

@questionnaire_bp.route('/<questionnaire_id>/submit', methods=['POST', 'OPTIONS'])
def submit_questionnaire(questionnaire_id):
    # Handle OPTIONS request for CORS preflight
    if request.method == 'OPTIONS':
        return '', 204
    
    """
    Submit answers for a questionnaire.
    """
    answers = request.json.get('answers', {})
    result = QuestionnaireService.submit_questionnaire(questionnaire_id, answers)
    if not result:
        return jsonify({'error': 'Questionnaire not found'}), 404
    return jsonify(result) 