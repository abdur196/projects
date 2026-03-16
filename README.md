
# MedVision AI - Medical Diagnosis Assistant

A web application for diagnosing medical conditions based on X-ray images and patient information.

## Project Overview

MedVision AI combines modern web technologies with AI capabilities to provide preliminary medical diagnosis based on X-ray images and patient-provided information:

- **Frontend:** React with ShadCN UI components and Tailwind CSS for a responsive, modern interface
- **Backend:** Flask API handling image uploads, patient data, and AI model interactions

## Features

- **X-ray Image Upload:** Upload chest X-ray images for AI analysis
- **Patient Information Form:** Enter relevant medical details to improve diagnosis accuracy
- **Diagnosis Results:** View AI-generated diagnosis with confidence scores for potential conditions
- **AI Chat Interface:** Discuss results with an AI assistant that provides contextual medical information

## Setup Instructions
- first of all download Ollama and run the following command
```
ollama run gemma3:4b
```

### Frontend (React)

1. Install dependencies:
```
npm install
```

2. Start the development server:
```
npm run dev
```

The frontend will be available at `http://localhost:8080`.

### Backend (Flask)

1. Navigate to the backend directory:
```
cd backend
```

2. Create a virtual environment:
```
python -m venv venv
```

3. Activate the virtual environment:
- On Windows: `venv\Scripts\activate`
- On macOS/Linux: `source venv/bin/activate`

4. Install dependencies:
```
pip install -r requirements.txt
```

5. Run the Flask server:
```
python app.py
```

The backend API will be available at `http://localhost:5000`.

## Important Notes

This application is for demonstration and educational purposes only. It is not intended for clinical use or to replace professional medical advice.

The AI diagnosis capabilities shown in this demo use mock data. In a production environment, these would be connected to properly trained and validated medical AI models.
