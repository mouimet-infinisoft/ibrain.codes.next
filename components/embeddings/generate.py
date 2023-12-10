import json
import torch
from transformers import AutoTokenizer, AutoModel

# Function to generate embeddings using CodeBERT
def generate_real_embedding(code_str):
    tokenizer = AutoTokenizer.from_pretrained("microsoft/codebert-base")
    model = AutoModel.from_pretrained("microsoft/codebert-base")

    inputs = tokenizer(code_str, return_tensors="pt", truncation=True, max_length=512)

    with torch.no_grad():
        outputs = model(**inputs)
        embeddings = outputs.last_hidden_state.mean(dim=1)

    return embeddings.cpu().numpy().tolist()

# Recursive function to traverse the graph and generate embeddings
def generate_embeddings_for_json(json_object):
    if isinstance(json_object, dict):
        for key, value in json_object.items():
            if key == 'functionsInfo':
                for function_info in value:
                    code_str = function_info.get('content', '')
                    function_info['real_embedding'] = generate_real_embedding(code_str)
            else:
                generate_embeddings_for_json(value)
    elif isinstance(json_object, list):
        for item in json_object:
            generate_embeddings_for_json(item)

# Load the JSON file
with open('input.json', 'r') as file:
    json_input = json.load(file)

# Generate real embeddings for the JSON input
generate_embeddings_for_json(json_input)

# Save the updated JSON object back to a file
with open('output.json', 'w') as file:
    json.dump(json_input, file, indent=2)
