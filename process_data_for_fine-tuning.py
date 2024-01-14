import json
import os

def process_data(folder_path, k):
    output_file = f'processed{k}.jsonl'
    prompt = "[INST] You are a modeling expert for modeling optimization problems. Based on the problem description provided to you, you might or might not want to ask clarifying questions about it. [/INST]"
    
    with open(output_file, 'w') as out:
        for i in range(1, k+1):
            file_path = os.path.join(folder_path, f'index{i}.json')
            if os.path.exists(file_path):
                with open(file_path, 'r') as file:
                    data = json.load(file)
                    questions = data["questions"]
                    for question in questions:
                        vague_description = "<human> " + question["vague_problem_description"]
                        clarifying_question = "<bot> " + question["clarifying_question"]
                        combined_text = f"{prompt} {vague_description} {clarifying_question}"
                        json.dump({"text": combined_text}, out)
                        out.write('\n')
            else:
                print(f"File not found: {file_path}")

# Usage
folder_path = './dataset'  # Replace with your dataset folder path
k = 56  # Replace with the number of files you want to process
process_data(folder_path, k)
