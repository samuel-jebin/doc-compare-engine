import re
from bs4 import BeautifulSoup


def read_txt_locally(filepath):
    with open(filepath,"r",encoding="utf-8") as reader:
        return reader.read()

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
    module_pattern = re.compile(r'.*\bmodule\b.*', re.IGNORECASE)

    html_lines = ['<html>', '<body>', '<form>']

    current_question_id = None
    current_question_html = None
    question_counter = 0

    for line in lines:
        line = line.strip()
        if not line:
            continue

        if module_pattern.match(line):
            html_lines.append(f"<h2>{line}</h2>")
            continue

        q_match = question_pattern.match(line)
        o_match = option_pattern.match(line)

        # Start of a new question
        if q_match:
            if current_question_html:
                html_lines.append(current_question_html)

            current_question_id = q_match.group(1).strip().rstrip(".")
            question_text = q_match.group(4).strip()
            question_counter += 1
            current_question_html = f'<div class="question-{question_counter}"><p><strong>{current_question_id}.</strong> {question_text}</p>'
            continue

        # Option line
        elif o_match and current_question_id:
            option_id = o_match.group(1)
            option_text = o_match.group(2)
            option_class = f"option -{question_counter}{option_id}"
            radio_html = (
                f'<div class="{option_class}">'
                f'<input type="radio" id="{current_question_id}_{option_id}" '
                f'name="{current_question_id}" value="{option_id}">'
                f'<label for="{current_question_id}_{option_id}">{option_id}. {option_text}</label>'
                f'</div>'
            )
            current_question_html += radio_html
            continue

        # Continuation lines
        elif current_question_html:
            if current_question_html.strip().endswith('</div>'):
                # Append to last option (inside label)
                current_question_html = re.sub(
                    r'(</label></div>)$',
                    f' {line}\\1',
                    current_question_html
                )
            else:
                # Append to question paragraph
                current_question_html = re.sub(
                    r'(</p>)$',
                    f' {line}\\1',
                    current_question_html
                )

    if current_question_html:
        html_lines.append(current_question_html)

    html_lines.append('<button type="submit">Submit</button>')
    html_lines += ['</form>', '</body>', '</html>']

    return "\n".join(html_lines)

def save_htmlfile(html_content,output_path):
    soup = BeautifulSoup(html_content,"html.parser")
    pretty_html = soup.prettify()
    
    with open(output_path,"w",encoding="utf-8") as filesaver:
        filesaver.write(pretty_html)
    print("HTML File save successfully")

if __name__=="__main__":
    file_path = r"C:\CursoryTech POC\pdftxt(crop).txt"
    textcontent = read_txt_locally(file_path)
    cleaned_text = preprocess_txt(textcontent)
    htmlcontent = txt_to_html_form(cleaned_text)
    save_htmlfile(htmlcontent,"v2_html.html")
    print(htmlcontent)
    
    
    