import torch
import torchxrayvision as xrv
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import io
import base64

chexnet_labels = [
    "No Finding", "Enlarged Cardiomediastinum", "Cardiomegaly", "Lung Opacity", "Lung Lesion", "Edema",
    "Consolidation", "Pneumonia", "Atelectasis", "Pneumothorax", "Pleural Effusion", "Pleural Other",
    "Fracture", "Support Devices"
]

# Load a pretrained model (DenseNet121 trained on CheXpert)
model = xrv.models.DenseNet(weights="densenet121-res224-chex")

# Set model to evaluation mode
model.eval()


def load_image(path):
    img = Image.open(path).convert("L")  # Grayscale
    img = img.resize((224, 224))
    img = np.array(img).astype(np.float32)
    # Rescale from [0, 255] to [-1024, 1024]
    img = img / 255.0 * (1024 + 1024) - 1024
    img = img[None, :, :]  # Add channel dimension
    img = torch.from_numpy(img).float()
    img = img.unsqueeze(0)  # Add batch dimension
    return img



def predict_chexnet(img_path, age, sex, view, projection, target_size=(224, 224)):
    # Load and preprocess image
    img = load_image(img_path)

    # Predict
    with torch.no_grad():
        predictions = model(img)[0].numpy()
    print("Raw predictions:", predictions)

    # Prepare results
    results = []
    for i, label in enumerate(model.pathologies):
        if label:
            results.append({
                'ailment': label,
                'confidence': float(predictions[i]),
                'description': ''  # Optionally add descriptions
            })

    # Visualization (as base64) - Table only
    fig, ax = plt.subplots(figsize=(6, 5))
    data = []
    for i, label in enumerate(model.pathologies):
        if label:
            pred_prob = predictions[i]
            data.append([label, f"{pred_prob:.3f}"])
    col_labels = ["Pathology", "Prediction"]
    table = ax.table(cellText=data, colLabels=col_labels, loc='center')
    table.auto_set_font_size(False)
    table.set_fontsize(8)
    ax.axis('off')
    plt.title(f"Patient Info - Age: {age}, Sex: {sex}, View: {view}, Projection: {projection}", fontsize=12)
    plt.tight_layout()

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    vis_base64 = base64.b64encode(buf.read()).decode('utf-8')
    plt.close()

    return {
        'results': results,
        'visualization': vis_base64
    }