from flask import Flask
from flask_cors import CORS
from app.routes.task_routes import task_bp
from app.routes.questionnaire_routes import questionnaire_bp
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# Register blueprints
app.register_blueprint(task_bp, url_prefix='/api/tasks')
app.register_blueprint(questionnaire_bp, url_prefix='/api/questionnaires')

@app.route('/api/health', methods=['GET'])
def health_check():
    return {'status': 'healthy'}, 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5000))) 