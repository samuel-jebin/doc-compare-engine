import re
from bs4 import BeautifulSoup


# def read_txt_locally(filepath):
#     with open(filepath,"r",encoding="utf-8") as reader:
#         return reader.read()

def preprocess_txt(raw_text):
    cleaned_lines = []
    for line in raw_text.splitlines():
        if "module" in line.lower():
            continue  # Skip lines with 'module'
        cleaned_line = re.sub(r'\[[^\[\]]*\]', '', line)
        cleaned_lines.append(cleaned_line)
    return "\n".join(cleaned_lines)

def txt_to_html_form(text):
    lines = text.strip().splitlines()
    question_pattern = re.compile(r"^((Q|S)\d+(-\d+)?\.)\s+(.*)")
    option_pattern = re.compile(r'^([A-Z\d]{1,3})[.)]\s+(.*)')

    html_lines = ['<html>', '<body>']

    current_question_id = None
    current_question_html = ""
    question_counter = 0

    for line in lines:
        line = line.strip()
        if not line:
            continue

        # Detect question line
        q_match = question_pattern.match(line)
        if q_match:
            if current_question_html:
                html_lines.append(current_question_html + '</div>')
            current_question_id = q_match.group(1).strip().rstrip(".")
            question_text = q_match.group(4).strip()
            question_counter += 1
            current_question_html = (
                f'<div class="question-{question_counter}">'
                f'<p><strong>{current_question_id}.</strong> {question_text}</p>'
            )
            continue

        # Detect option line
        o_match = option_pattern.match(line)
        if o_match and current_question_id:
            option_id = o_match.group(1)
            option_text = o_match.group(2)
            radio_html = (
                f'<div class="option">'
                f'<input type="radio" id="{current_question_id}_{option_id}" '
                f'name="{current_question_id}" value="{option_id}"> '
                f'<label for="{current_question_id}_{option_id}">{option_id}. {option_text}</label>'
                f'</div>'
            )
            current_question_html += radio_html
            continue

        # Handle continuation line
        if current_question_html:
            if 'input type="radio"' in current_question_html:
                # Append to last option's label
                current_question_html = re.sub(
                    r'(</label></div>)$',
                    f' {line}\\1',
                    current_question_html
                )
            else:
                # Append to question text
                current_question_html = re.sub(
                    r'(</p>)$',
                    f' {line}\\1',
                    current_question_html
                )

    # Final append
    if current_question_html:
        html_lines.append(current_question_html + '</div>')

    html_lines += ['</body>', '</html>']
    return "\n".join(html_lines)

# def save_htmlfile(html_content,output_path):
#     soup = BeautifulSoup(html_content,"html.parser")
#     pretty_html = soup.prettify()
    
#     with open(output_path,"w",encoding="utf-8") as filesaver:
#         filesaver.write(pretty_html)
#     print("HTML File save successfully")

# if __name__=="__main__":
#     file_path = r"C:\CursoryTech POC\pdf-text(form-recg).txt"
#     textcontent = read_txt_locally(file_path)
#     cleaned_text = preprocess_txt(textcontent)
#     htmlcontent = txt_to_html_form(cleaned_text)
#     save_htmlfile(htmlcontent,"html_output.html")
#     print(htmlcontent)
    
    
    