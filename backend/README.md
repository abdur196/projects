
# MedVision AI Backend

This directory contains the Flask backend for the MedVision AI medical diagnosis application.

## Setup

1. Create a virtual environment:
```
python -m venv venv
```

2. Activate the virtual environment:
- On Windows: `venv\Scripts\activate`
- On macOS/Linux: `source venv/bin/activate`

3. Install dependencies:
```
pip install -r requirements.txt
```

4. Run the Flask server:
```
python app.py
```

The server will be available at `http://localhost:5000`.

## API Endpoints

- `POST /api/upload-xray` - Upload an X-ray image
- `POST /api/patient-data` - Submit patient information
- `GET /api/diagnosis/<session_id>` - Retrieve diagnosis results
- `POST /api/chat/<session_id>` - Send a message to the AI chatbot

## Development

This is a mock implementation. In a production environment, you would need to:

1. Implement actual machine learning models in `load_model.py`
2. Connect to a real language model API in `LLM.py`
3. Use a proper database for session storage
4. Set up proper authentication and security measures
5. Deploy to a production server with WSGI
