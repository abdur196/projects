from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import uuid
from werkzeug.utils import secure_filename
import time

# Import the actual ML modules
import LLM
from chexnet_model import predict_chexnet

app = Flask(__name__)
CORS(app)  # Allow cross-origin requests

# Configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max upload

# Helper functions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Mock database for sessions (in production, use a real database)
sessions = {}

# Routes
@app.route('/api/upload-xray', methods=['POST'])
def upload_xray():
    """Handle X-ray image upload"""
    if 'xray' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['xray']
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file and allowed_file(file.filename):
        # Create a unique session ID
        session_id = str(uuid.uuid4())
        
        # Save the uploaded file
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{session_id}_{filename}")
        file.save(file_path)
        
        # Store session info
        sessions[session_id] = {
            'xray_path': file_path,
            'created_at': time.time(),
            'patient_data': None,
            'diagnosis_results': None,
            'visualization': None
        }
        
        return jsonify({
            'success': True, 
            'sessionId': session_id,
            'message': 'X-ray uploaded successfully'
        })
    
    return jsonify({'error': 'Invalid file format'}), 400

@app.route('/api/patient-data', methods=['POST'])
def submit_patient_data():
    """Handle patient data submission"""
    data = request.json
    session_id = data.get('sessionId')
    
    if not session_id or session_id not in sessions:
        return jsonify({'error': 'Invalid or expired session'}), 400
    
    # Store patient data in session
    sessions[session_id]['patient_data'] = {
        'age': data.get('age'),
        'sex': data.get('sex'),
        'frontalLateral': data.get('frontalLateral', 'Frontal'),
        'apPa': data.get('apPa', 'PA')
    }
    
    # Use the CheXNet Keras model for prediction
    try:
        prediction_data = predict_chexnet(
            img_path=sessions[session_id]['xray_path'],
            age=sessions[session_id]['patient_data']['age'],
            sex=sessions[session_id]['patient_data']['sex'],
            view=sessions[session_id]['patient_data']['frontalLateral'],
            projection=sessions[session_id]['patient_data']['apPa']
        )
        
        # Store diagnosis results and visualization
        sessions[session_id]['diagnosis_results'] = prediction_data['results']
        sessions[session_id]['visualization'] = prediction_data['visualization']
        
        return jsonify({
            'success': True,
            'results': prediction_data['results'],
            'visualization': prediction_data['visualization']
        })
    except Exception as e:
        print(f"Error during prediction: {str(e)}")
        return jsonify({'error': f'Prediction failed: {str(e)}'}), 500

@app.route('/api/diagnosis/<session_id>', methods=['GET'])
def get_diagnosis(session_id):
    """Retrieve diagnosis results for a session"""
    if session_id not in sessions:
        return jsonify({'error': 'Invalid or expired session'}), 400
    
    if not sessions[session_id].get('diagnosis_results'):
        return jsonify({'error': 'Diagnosis not yet performed'}), 404
    
    # Return the diagnosis results with visualization
    return jsonify({
        'success': True,
        'results': sessions[session_id]['diagnosis_results'],
        'visualization': sessions[session_id]['visualization']
    })

@app.route('/api/chat/<session_id>', methods=['POST'])
def chat_with_ai(session_id):
    """Handle AI chat interaction"""
    if session_id not in sessions:
        return jsonify({'error': 'Invalid or expired session'}), 400
    
    if not sessions[session_id]['diagnosis_results'] or not sessions[session_id]['patient_data']:
        return jsonify({'error': 'Diagnosis or patient data missing'}), 400
    
    data = request.json
    user_message = data.get('message', '')
    
    if not user_message:
        return jsonify({'error': 'Empty message'}), 400
    
    # Use the real LLM module for response generation
    try:
        ai_response = LLM.generate_response(
            user_message=user_message,
            diagnosis_results=sessions[session_id]['diagnosis_results'],
            patient_data=sessions[session_id]['patient_data'],
        )
        
        if not ai_response:
            # Fallback if LLM fails or is unavailable
            ai_responses = [
                "Based on your X-ray, I can see signs consistent with the findings in our analysis. Could you tell me more about your symptoms?",
                "The X-ray findings suggest some abnormalities that align with the diagnosis. How long have you been experiencing these symptoms?",
                "I notice the model has detected some patterns in your X-ray. Would you like me to explain what these specific findings mean?",
                "Based on the analysis and your medical history, there are several factors to consider. What concerns you most about these results?",
                "The analysis shows some findings that should be discussed with a healthcare provider. Is there anything specific about the results you'd like me to clarify?"
            ]
            import random
            ai_response = random.choice(ai_responses)
        
        return jsonify({
            'success': True,
            'message': ai_response,
            'timestamp': time.time()
        })
    except Exception as e:
        print(f"Error generating AI response: {str(e)}")
        return jsonify({'error': f'AI response generation failed: {str(e)}'}), 500

# Cleanup old sessions periodically (in production, this would be a scheduled task)
@app.before_request
def cleanup_old_sessions():
    """Remove sessions older than 1 hour"""
    current_time = time.time()
    expired_sessions = []
    
    for session_id, session_data in sessions.items():
        if current_time - session_data['created_at'] > 3600:  # 1 hour
            expired_sessions.append(session_id)
            
            # Remove the uploaded file
            if os.path.exists(session_data['xray_path']):
                os.remove(session_data['xray_path'])
    
    for session_id in expired_sessions:
        sessions.pop(session_id, None)

# Serve uploaded files (for development only)
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)
