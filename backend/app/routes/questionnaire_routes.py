from flask import Flask, Blueprint, request, jsonify
from datetime import datetime
from bson import ObjectId
from app.models.questionnaire import (
    Questionnaire, 
    questionnaire_collection, 
    questionnaires
)
from app.services.questionnaire_service import QuestionnaireService
from flask_cors import CORS
from dotenv import load_dotenv

questionnaire_bp = Blueprint('questionnaire', __name__)

# Load environment variables
load_dotenv()
app = Flask(__name__)
# Configure CORS to allow all origins, methods, and headers
CORS(app, resources={r"/*": {
    "origins": "*",
    "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    "allow_headers": ["Content-Type", "Authorization", "X-Requested-With"]
}}, supports_credentials=True)

def use_mongodb():
    """Check if MongoDB is available"""
    return 'questionnaire_collection' in globals() and questionnaire_collection is not None

@questionnaire_bp.route('/', methods=['POST', 'OPTIONS'])
@questionnaire_bp.route('', methods=['POST', 'OPTIONS'])
def create_questionnaire():
    # Handle OPTIONS request for CORS preflight
    if request.method == 'OPTIONS':
        return '', 204
    
    try:
        data = request.get_json()
        questionnaire = Questionnaire(**data)
        
        if use_mongodb():
            result = questionnaire_collection.insert_one(questionnaire.to_mongo())
            questionnaire.id = str(result.inserted_id)
        else:
            questionnaire.id = str(ObjectId())
            questionnaires.append(questionnaire.dict())
            
        return jsonify(questionnaire.dict()), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@questionnaire_bp.route('/', methods=['GET'])
def get_questionnaires():
    try:
        if use_mongodb():
            items = [
                Questionnaire.from_mongo(q).dict() 
                for q in questionnaire_collection.find()
            ]
        else:
            items = questionnaires
            
        return jsonify(items), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@questionnaire_bp.route('/<questionnaire_id>', methods=['GET'])
def get_questionnaire(questionnaire_id):
    try:
        if use_mongodb():
            item = questionnaire_collection.find_one({"_id": ObjectId(questionnaire_id)})
            if item:
                return jsonify(Questionnaire.from_mongo(item).dict()), 200
        else:
            item = next((q for q in questionnaires if q['id'] == questionnaire_id), None)
            if item:
                return jsonify(item), 200
                
        return jsonify({"error": "Questionnaire not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@questionnaire_bp.route('/<questionnaire_id>', methods=['PUT'])
def update_questionnaire(questionnaire_id):
    try:
        data = request.get_json()
        data['id'] = questionnaire_id
        questionnaire = Questionnaire(**data)
        
        if use_mongodb():
            result = questionnaire_collection.replace_one(
                {"_id": ObjectId(questionnaire_id)},
                questionnaire.to_mongo()
            )
            if result.modified_count:
                return jsonify(questionnaire.dict()), 200
        else:
            index = next((i for i, q in enumerate(questionnaires) 
                         if q['id'] == questionnaire_id), None)
            if index is not None:
                questionnaires[index] = questionnaire.dict()
                return jsonify(questionnaire.dict()), 200
                
        return jsonify({"error": "Questionnaire not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@questionnaire_bp.route('/<questionnaire_id>', methods=['DELETE'])
def delete_questionnaire(questionnaire_id):
    try:
        if use_mongodb():
            result = questionnaire_collection.delete_one({"_id": ObjectId(questionnaire_id)})
            if result.deleted_count:
                return jsonify({"message": "Questionnaire deleted successfully"}), 200
        else:
            initial_length = len(questionnaires)
            questionnaires[:] = [q for q in questionnaires if q['id'] != questionnaire_id]
            if len(questionnaires) < initial_length:
                return jsonify({"message": "Questionnaire deleted successfully"}), 200
                
        return jsonify({"error": "Questionnaire not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@questionnaire_bp.route('/<questionnaire_id>/status', methods=['PUT'])
def update_status(questionnaire_id):
    try:
        data = request.get_json()
        new_status = data.get('status')
        
        if use_mongodb():
            result = questionnaire_collection.update_one(
                {"_id": ObjectId(questionnaire_id)},
                {"$set": {"status": new_status}}
            )
            if result.modified_count:
                updated = questionnaire_collection.find_one({"_id": ObjectId(questionnaire_id)})
                return jsonify(Questionnaire.from_mongo(updated).dict()), 200
        else:
            questionnaire = next((q for q in questionnaires if q['id'] == questionnaire_id), None)
            if questionnaire:
                questionnaire['status'] = new_status
                return jsonify(questionnaire), 200
                
        return jsonify({"error": "Questionnaire not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 400

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
