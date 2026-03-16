import requests
import base64
import json

# Load and encode image as base64
def encode_image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

# Query Ollama with or without image
def query_ollama(prompt, image_path=None):
    payload = {
        "model": "gemma3:4b",
        "prompt": prompt
    }

    if image_path:
        image_base64 = encode_image_to_base64(image_path)
        payload["images"] = [image_base64]

    response = requests.post("http://localhost:11434/api/generate", json=payload, stream=True)

    if response.status_code == 200:
        full_response = ""
        for line in response.iter_lines():
            if line:
                try:
                    json_data = json.loads(line.decode("utf-8"))
                    full_response += json_data.get("response", "")
                except json.JSONDecodeError as e:
                    print("Decode error:", e)
        return full_response
    else:
        print("Error:", response.status_code, response.text)
        return None

def generate_response(user_message, diagnosis_results, patient_data):
    """
    Generate a contextual response based on the user's message and the diagnosis context.
    
    Args:
        user_message (str): The user's message/question
        diagnosis_results (list): The diagnosis results from the model
        patient_data (dict): The patient information
        
    Returns:
        str: AI-generated response
    """
    # Format the context information into a detailed prompt for the LLM
    base_prompt  = f"""
    You are a medical AI assistant that explains X-ray diagnosis results to patients.
    Be professional, brief, and avoid unnecessary details. Always limit explanations to 2–3 sentences per ailment.
    Do not continue unless the user asks questions.

    PATIENT INFORMATION:
    - Age: {patient_data.get('age', 'Unknown')}
    - Gender: {patient_data.get('sex', 'Unknown')}
    - X-ray Type: {patient_data.get('frontalLateral', 'Unknown')}
    - View: {patient_data.get('apPa', 'Unknown')}

    DIAGNOSIS RESULTS:
    """

    for result in diagnosis_results:
        base_prompt += f"- {result['ailment']}: {result['confidence']:.2f} probability\n"

    if user_message.strip():
        # User asked a question — answer briefly and specifically
        prompt = base_prompt + f"\nUSER QUESTION: {user_message}\n\nRespond with no more than 40 words. Be precise and medically sound."
    else:
        # No user question — explain each condition briefly
        prompt = base_prompt + "\nBriefly explain each ailment listed above with probability greater than 0.5 (2–3 sentences each). Then stop and wait for user input."

    return query_ollama(prompt)
