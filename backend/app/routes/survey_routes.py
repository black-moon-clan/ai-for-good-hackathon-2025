from flask import Blueprint, request, jsonify
from app.services.survey_service import SurveyService

survey_bp = Blueprint('survey', __name__)

@survey_bp.route('', methods=['POST'])
def create_task():
    print("Creating survey answer")
    survey_data = request.json
    survey = SurveyService.create_survey(survey_data)
    return jsonify(survey), 201
