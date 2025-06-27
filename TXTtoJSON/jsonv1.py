import re
import json
import uuid

def generate_random_id():
    return str(uuid.uuid4())[:8]
    
# def get_txt_locally(txt_file_path):
    
#     with open(txt_file_path, "r", encoding="utf-8") as f:
#         raw_text = f.read()
#     return raw_text


def preprocess_text(raw_text):
#    cleaned_text = re.sub(r'\[[^\[\]]*\]', '', raw_text)
#    return cleaned_text
    cleaned_lines = []
    for line in raw_text.splitlines():
        if "module" in line.lower():
            continue 
        cleaned_line = re.sub(r'\[[^\[\]]*\]', '', line)
        cleaned_lines.append(cleaned_line)
    return "\n".join(cleaned_lines)

def convert_txt_json(text):
    
    questions = []
    lines = text.strip().splitlines()
    question_pattern = re.compile(r"^((Q|S)\d+(-\d+)?\.)\s+(.*)")
    option_pattern = re.compile(r'^([A-Z\d]{1,3})[.)]\s+(.*)')

    current_question = None

    for line in lines:
        line = line.strip()
        if not line:
            continue

        q_match = question_pattern.match(line)
        o_match = option_pattern.match(line)

        # Detect question
        if q_match:
            if current_question:
                questions.append(current_question)
            question_number = q_match.group(1).strip()
            question_text = q_match.group(4).strip()
            current_question = {
                "questionId":generate_random_id(),
                "questionNumber": question_number,
                "questionContent": question_text,
                "options": []
            }
        # Detect option
        elif o_match and current_question:
            option_text = f"{o_match.group(1)}. {o_match.group(2)}"
            current_question["options"].append(option_text)
        # Handle non-prefixed option lines or continuation lines
        elif current_question:
            if current_question["options"]:
                # Append as continuation of last option
                current_question["options"][-1] += " " + line
            else:
                current_question["questionContent"] += " " + line

    # Append the last question
    if current_question:
        questions.append(current_question)
    # print(json.dumps(questions,indent=4))
    return json.dumps(questions,indent=4)

# def save_to_file(data,fileName):
#     with open(fileName,"w",encoding="utf-8") as f:
#         json.dump(data,f,indent=4)
#     print("JSON Saved successfully")
    

# if __name__ == "__main__":
# # Example usage
# txt_file_path = r"C:\CursoryTech POC\pdf-text(form-recg).txt"
# raw_text = get_txt_locally(txt_file_path)
# convert_txt_json(raw_text)
#     cleaned_text = preprocess_text(raw_text)
#     formatted_json = parse_survey(cleaned_text)

#     # Print or save
#     print(json.dumps(formatted_json, indent=4))
#     save_to_file(formatted_json,fileName="output_formatted_final.json")