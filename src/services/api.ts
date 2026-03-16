import axios from 'axios';

// API base URL - change this to your Flask backend URL when deploying
const API_BASE_URL = 'http://localhost:5000';

// Configure axios instance
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// API function to upload X-ray image
export const uploadXRayImage = async (file: File) => {
  const formData = new FormData();
  formData.append('xray', file);
  
  try {
    const response = await api.post('/api/upload-xray', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  } catch (error) {
    console.error('Error uploading X-ray image:', error);
    throw error;
  }
};

// API function to submit patient data
export const submitPatientData = async (patientData: PatientData) => {
  try {
    const response = await api.post('/api/patient-data', patientData);
    return response.data;
  } catch (error) {
    console.error('Error submitting patient data:', error);
    throw error;
  }
};

// API function to get diagnosis results
export const getDiagnosisResults = async (sessionId: string) => {
  try {
    const response = await api.get(`/api/diagnosis/${sessionId}`);
    return response.data;
  } catch (error) {
    console.error('Error getting diagnosis results:', error);
    throw error;
  }
};

// API function to send message to AI chat
export const sendChatMessage = async (sessionId: string, message: string) => {
  try {
    const response = await api.post(`/api/chat/${sessionId}`, { message });
    return response.data;
  } catch (error) {
    console.error('Error sending chat message:', error);
    throw error;
  }
};

// Types
export interface PatientData {
  age: number;
  sex: string;
  sessionId?: string;
  frontalLateral?: string;
  apPa?: string;
}

export interface DiagnosisResult {
  ailment: string;
  confidence: number;
  description: string;
}

export interface DiagnosisResponse {
  results: DiagnosisResult[];
  visualization?: string;
}

export interface ChatMessage {
  role: 'user' | 'assistant';
  content: string;
  timestamp: string;
}

export default api;
