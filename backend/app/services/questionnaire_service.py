from flask import Blueprint, request, jsonify
from datetime import datetime
import uuid
import os
import json
from pathlib import Path
from bson import ObjectId
from app.models.questionnaire import questionnaire_collection, Questionnaire

class QuestionnaireService:
    @staticmethod
    def start_questionnaire(questionnaire_id):
        """
        Generate Python code for a questionnaire flow and save it to a file.
        """
        # Find the questionnaire by ID using MongoDB
        try:
            questionnaire_doc = questionnaire_collection.find_one({"_id": ObjectId(questionnaire_id)})
            if not questionnaire_doc:
                return None
            
            # Convert MongoDB document to Questionnaire object
            questionnaire = Questionnaire.from_mongo(questionnaire_doc)
            
            # Generate Python code for the questionnaire flow
            python_code = QuestionnaireService._generate_flow_code(questionnaire.dict())
            
            # Create directory if it doesn't exist
            flows_dir = Path("flows")
            flows_dir.mkdir(exist_ok=True)
            
            # Save the code to a file
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            questionnaire_name = questionnaire.title.replace(' ', '_').lower()
            
            filename = f"{questionnaire_name}_{timestamp}_flow.based"
            file_path = flows_dir / filename
            
            with open(file_path, 'w') as f:
                f.write(python_code)
            
            return {
                "questionnaire_id": questionnaire_id,
                "file_path": str(file_path),
                "status": "success",
                "message": "Questionnaire flow generated successfully"
            }
        except Exception as e:
            print(f"Error in start_questionnaire: {str(e)}")
            return None
    
    @staticmethod
    def _generate_flow_code(questionnaire):
        """
        Generate Python code for a questionnaire flow.
        """
        questions = questionnaire.get('questions', [])
        
        # Start with basic setup
        lines = []
        lines.append("state = {}")
        lines.append(f"meta_prompt = f\"Questionnaire: {questionnaire.get('title', '')}\"")
        lines.append("")
        
        # Process each question
        for i, question in enumerate(questions):
            question_id = f"q{i+1}"
            question_text = question.get('text', f'Question {i+1}')
            question_type = question.get('type', 'text')
            
            if question_type == 'rating':
                lines.append(f"loop:")
                lines.append(f'    {question_id}_response = talk("{question_text}", True)')
                lines.append(f'until "User has provided a rating between 1 to 5":')
                lines.append(f'    {question_id}_answer = _response.ask(')
                lines.append(f'        question="Based on the user\'s response, what rating did they give from 1 to 5?",')
                lines.append(f'        example={{"rating": 4}}')
                lines.append(f'    )')
                lines.append(f'state["{question_id}"] = {question_id}_answer["rating"]')
            else:
                lines.append(f"loop:")
                lines.append(f'    {question_id}_response = talk("{question_text}", True)')
                lines.append(f'until "User has provided an answer":')
                lines.append(f'    {question_id}_answer = _response.ask(')
                lines.append(f'        question="What is the user\'s response ?",')
                lines.append(f'        example={{"message": "User response"}}')
                lines.append(f'    )')
                lines.append(f'state["{question_id}"] = {question_id}_answer["message"]')
            
            lines.append("")
        
        lines.append('talk("Thank you for completing the questionnaire. Your responses have been recorded.")')
        
        return "\n".join(lines)
    
    @staticmethod
    def submit_questionnaire(questionnaire_id, answers):
        """
        Submit answers for a questionnaire.
        """
        try:
            # Find the questionnaire by ID using MongoDB
            questionnaire_doc = questionnaire_collection.find_one({"_id": ObjectId(questionnaire_id)})
            if not questionnaire_doc:
                return None
            
            # In a real application, you might store the answers in a database
            # For this example, we'll just return a success message
            return {
                "questionnaire_id": questionnaire_id,
                "status": "success",
                "message": "Questionnaire submitted successfully"
            }
        except Exception as e:
            print(f"Error in submit_questionnaire: {str(e)}")
            return None 