import torch
import numpy as np
import matplotlib.pyplot as plt
from torchvision import models, transforms
from torch import nn
from PIL import Image
import cv2
import os
import io
import base64

# Define CheXpert class labels
pathologies = [
    'No Finding', 'Enlarged Cardiomediastinum', 'Cardiomegaly',
    'Lung Opacity', 'Lung Lesion', 'Edema', 'Consolidation',
    'Pneumonia', 'Atelectasis', 'Pneumothorax',
    'Pleural Effusion', 'Pleural Other', 'Fracture', 'Support Devices'
]

# Get base directory
base_dir = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(base_dir, 'mobilenet_chexpert_best.pth')

# Set device and load trained model
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
mobilenet = models.mobilenet_v2(pretrained=False)
mobilenet.classifier[1] = nn.Linear(mobilenet.last_channel, 14)

# Try to load model
try:
    mobilenet.load_state_dict(torch.load(model_path, map_location=device))
    print(f"Model loaded successfully from {model_path}")
except Exception as e:
    print(f"Error loading model: {e}")
    print("Using untrained model for demonstration purposes")

mobilenet = mobilenet.to(device)
mobilenet.eval()

# Transform for single image - matching training transforms
transform = transforms.Compose([
    transforms.Resize((128, 128)),  # Match training size
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])  # ImageNet normalization
])

def predict_xray_probs(image_path, patient_data=None):
    """Get probabilities from model, incorporating patient metadata if available"""
    try:
        # Load and preprocess image
        image = Image.open(image_path).convert("RGB")
        input_tensor = transform(image).unsqueeze(0).to(device)

        # Prepare metadata tensor if available
        if patient_data:
            # Convert metadata to tensor
            age = torch.tensor([[float(patient_data.get('age', 0))]], device=device)
            sex = torch.tensor([[1.0 if patient_data.get('sex', '').lower() == 'male' else 0.0]], device=device)
            view = torch.tensor([[1.0 if patient_data.get('frontalLateral', 'Frontal') == 'Lateral' else 0.0]], device=device)
            technique = torch.tensor([[1.0 if patient_data.get('apPa', 'PA') == 'AP' else 0.0]], device=device)
            
            # Combine metadata
            metadata = torch.cat([age, sex, view, technique], dim=1)
            # Normalize age to [0,1] range (assuming max age of 100)
            metadata[:, 0] = metadata[:, 0] / 100.0
        else:
            metadata = torch.zeros((1, 4), device=device)

        with torch.no_grad():
            # Get image features
            image_features = mobilenet.features(input_tensor)
            image_features = mobilenet.avgpool(image_features)
            image_features = torch.flatten(image_features, 1)
            
            # Combine image features with metadata
            combined_features = torch.cat([image_features, metadata], dim=1)
            
            # Pass through classifier
            output = mobilenet.classifier(combined_features)
            probs = torch.sigmoid(output).cpu().numpy()[0]

        return probs
    except Exception as e:
        print(f"Error in prediction: {e}")
        return np.zeros(len(pathologies))

def predict(xray_path, patient_data):
    """
    Predict possible medical conditions based on X-ray image and patient data.
    
    Args:
        xray_path (str): Path to the uploaded X-ray image
        patient_data (dict): Patient information including age, sex, FrontalLateral, apPa
        
    Returns:
        dict: Contains ailments list and visualization image
    """
    # Get prediction probabilities with patient data
    probs = predict_xray_probs(xray_path, patient_data)
    
    # Create results
    results = []
    
    # Add diagnoses to results, focusing on conditions with higher probabilities
    for i, (pathology, prob) in enumerate(zip(pathologies, probs)):
        # Only include pathologies with probability > 0.1
        if prob > 0.1:
            # Add basic descriptions for common findings
            description = get_pathology_description(pathology)
            results.append({
                'ailment': pathology,
                'confidence': float(prob),
                'description': description
            })
    
    # Sort by confidence (highest first)
    results = sorted(results, key=lambda x: x['confidence'], reverse=True)
    
    # Generate visualization
    vis_base64 = generate_visualization(xray_path, probs)
    
    return {
        'results': results,
        'visualization': vis_base64
    }

def generate_visualization(image_path, probs):
    """Generate visualization of X-ray with prediction probabilities"""
    plt.figure(figsize=(10, 6))
    
    # Load and display the X-ray
    orig_img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if orig_img is None:
        orig_img = np.zeros((256, 256))  # Fallback if image can't be loaded
    else:
        orig_img = cv2.resize(orig_img, (256, 256))
    
    plt.subplot(1, 2, 1)
    plt.imshow(orig_img, cmap='gray')
    plt.title("Input X-ray", fontsize=12)
    plt.axis('off')
    
    # Display the prediction probabilities
    plt.subplot(1, 2, 2)
    plt.axis('off')
    
    prob_strings = [f"{p:.2f}" for p in probs]
    table = plt.table(
        cellText=np.array([pathologies, prob_strings]).T,
        colLabels=['Pathology', 'Predicted Probability'],
        loc='center',
        colWidths=[0.5, 0.5],
        cellLoc='center'
    )
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1, 1.5)
    plt.title("Model Predictions", pad=20)
    
    # Convert plot to base64 encoded image
    buf = io.BytesIO()
    plt.tight_layout()
    plt.savefig(buf, format='png')
    buf.seek(0)
    img_base64 = base64.b64encode(buf.read()).decode('utf-8')
    plt.close()
    
    return img_base64

def get_pathology_description(pathology):
    """Return description for common pathologies"""
    descriptions = {
        'No Finding': 'No abnormalities detected in the X-ray.',
        'Enlarged Cardiomediastinum': 'Widening of the central chest area that contains the heart and other structures.',
        'Cardiomegaly': 'Enlargement of the heart, which may indicate heart failure or other cardiac conditions.',
        'Lung Opacity': 'Area of reduced transparency in the lung field that may represent fluid, consolidation, or mass.',
        'Lung Lesion': 'Abnormal area or growth in the lung tissue that requires further investigation.',
        'Edema': 'Excess fluid in the lungs, often due to heart failure or other conditions.',
        'Consolidation': 'Lung tissue filled with liquid instead of air, often indicating pneumonia or other infection.',
        'Pneumonia': 'Inflammation of the lungs caused by infection.',
        'Atelectasis': 'Collapse or closure of a lung resulting in reduced or absent gas exchange.',
        'Pneumothorax': 'Presence of air in the pleural space causing lung collapse.',
        'Pleural Effusion': 'Buildup of fluid between the lungs and chest cavity.',
        'Pleural Other': 'Other abnormalities of the pleural space.',
        'Fracture': 'Break in bone structure visible on the X-ray.',
        'Support Devices': 'Medical devices visible in the X-ray such as tubes, lines, or pacemakers.'
    }
    return descriptions.get(pathology, 'No description available.')
