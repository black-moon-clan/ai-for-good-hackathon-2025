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
        Then deploy it using Brainbase Labs SDK.
        """
        try:
            questionnaire_doc = questionnaire_collection.find_one({"_id": ObjectId(questionnaire_id)})
            if not questionnaire_doc:
                return None
            
            questionnaire = Questionnaire.from_mongo(questionnaire_doc)
            python_code = QuestionnaireService._generate_flow_code(questionnaire.dict())
            
            flows_dir = Path("flows")
            flows_dir.mkdir(exist_ok=True)
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            questionnaire_name = questionnaire.title.replace(' ', '_').lower()
            
            filename = f"{questionnaire_name}_{timestamp}_flow.based"
            file_path = flows_dir / filename
            
            with open(file_path, 'w') as f:
                f.write(python_code)
            
            # Deploy the flow using Brainbase Labs SDK
            from brainbase_labs import BrainbaseLabs
            
            # Initialize Brainbase Labs SDK
            bb = BrainbaseLabs(api_key=os.getenv("BRAINBASE_LABS_API_KEY"))
            
            # Create or get Twilio integration
            # twilio_integration = bb.team.integrations.twilio.create(
            #     account_sid=os.getenv("TWILIO_ACCOUNT_SID"),
            #     auth_token=os.getenv("TWILIO_AUTH_TOKEN")
            # )
            
            # Get phone number from environment or configuration
            raw_phone_number = os.getenv("TWILIO_PHONE_NUMBER")
            
            # Create a worker for this questionnaire
            worker = bb.workers.create(
                name=f"Questionnaire: {questionnaire.title}",
                description=f"A questionnaire assistant for {questionnaire.title}",
                status="active"
            )
            
            # Create a flow for the worker
            flow = bb.workers.flows.create(
                worker_id=worker.id,
                name=questionnaire.title,
                path=str(file_path),
                label="v1",
                validate=False
            )
            
            # Deploy the flow to a voice channel
            voice_deployment = bb.workers.deployments.voice.create(
                worker_id=worker.id,
                name=f"{questionnaire.title} Voice Deployment",
                flow_id=flow.id,
                phone_number=raw_phone_number,
                config={}
            )
            
            deployment_status = "success" if voice_deployment else "failed"
            deployment_message = f"Deployed to {voice_deployment.phone_number}" if voice_deployment else "Deployment failed"
            
            print('successfully deployed questionnaire')
            return {
                "questionnaire_id": questionnaire_id,
                "file_path": str(file_path),
                "status": "success",
                "message": "Questionnaire flow generated successfully",
                "deployment": {
                    "status": deployment_status,
                    "message": deployment_message,
                    "worker_id": worker.id if worker else None,
                    "flow_id": flow.id if flow else None,
                    "deployment_id": voice_deployment.id if voice_deployment else None,
                    "phone_number": voice_deployment.phone_number if voice_deployment else None
                }
            }
        except Exception as e:
            print(f"Error in start_questionnaire: {str(e)}")
            return {
                "questionnaire_id": questionnaire_id,
                "status": "error",
                "message": f"Error: {str(e)}"
            }
    
    @staticmethod
    def _generate_flow_code(questionnaire):
        """
        Generate Python code for a questionnaire flow.
        """
        questions = questionnaire.get('questions', [])
        
        # Start with basic setup
        lines = []
        lines.append("state = {}")
        lines.append(f"meta_prompt = f\"{questionnaire.get('title', '')}\"")
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
                lines.append(f'    {question_id}_answer = {question_id}_response.ask(')
                lines.append(f'        question="Based on the user\'s response, what rating did they give from 1 to 5?",')
                lines.append(f'        example={{"rating": 4}}')
                lines.append(f'    )')
                lines.append(f'state["{question_id}"] = {question_id}_answer["rating"]')
            else:
                lines.append(f"loop:")
                lines.append(f'    {question_id}_response = talk("{question_text}", True)')
                lines.append(f'until "User has provided an answer":')
                lines.append(f'    {question_id}_answer = {question_id}_response.ask(')
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