from bs4 import BeautifulSoup
import re

# # htmlFile_path = r"C:\CursoryTech POC\TXTtoHTML\html_output.html"
# # with open(htmlFile_path,"r") as htmlReader:
# #      result = htmlReader.read()

# def preprocess_txt_file():
         
#     txtFile_path = r"C:\CursoryTech POC\pdftxt(crop).txt"
#     with open(txtFile_path,"r") as txt_reader:
#         result_1 = txt_reader.read()
        
#     cleaned_lines = []
#     for line in result_1.splitlines():
#         if "module" in line.lower():
#             continue 
#         cleaned_line = re.sub(r'\[[^\[\]]*\]', '', line)
#         cleaned_lines.append(cleaned_line)
#     # print("\n".join(cleaned_lines))
#     result = "\n".join(cleaned_lines)
#     output_path  = "preprocess-txt.txt"
#     with open (output_path,"w",encoding = "utf-8") as filewriter:
#         filewriter.write(result)
#     return "\n".join(cleaned_lines)
    
    
    
# # preprocess_txt_file()



# def preprocess_html_file(html_text):
   
#     soup = BeautifulSoup(html_text, "html.parser")
#     question_blocks = soup.find_all("div", class_="question", recursive=True)

#     structured_output = ""
#     seen_questions = set()  # To prevent duplicates

#     for block in question_blocks:
#         p_tag = block.find("p")
#         if not p_tag:
#             continue

#         strong_tag = p_tag.find("strong")
#         question_number = strong_tag.get_text(strip=True).rstrip('.') if strong_tag else "N/A"
#         question_text = p_tag.get_text(strip=True).replace(strong_tag.get_text(strip=True), "", 1).strip()

#         # Combine both for uniqueness
#         question_key = f"{question_number}|{question_text}"
#         if question_key in seen_questions:
#             continue
#         seen_questions.add(question_key)

#         option_divs = [div for div in block.find_all("div", class_="option", recursive=False)]
#         options = []
#         for option in option_divs:
#             label = option.find("label")
#             if label:
#                 options.append(label.get_text(strip=True))

#         structured_output += f"Question Number: {question_number}\n"
#         structured_output += f"Question: {question_text}\n"
#         structured_output += "Options:\n" + "\n".join(options) + "\n\n"
#     print(structured_output)
#     return structured_output


def extract_questions_from_html(html_content):
    
    soup = BeautifulSoup(html_content, 'html.parser')
    output_result = []
    
    # with open(output_path, 'w', encoding='utf-8') as out:
    questions = soup.find_all('div', class_=lambda x: x and x.startswith('question-'))

    for q_div in questions:
            p_tag = q_div.find('p')
            if not p_tag or not p_tag.find('strong'):
                continue

            # Extract question number and content
            question_number = p_tag.find('strong').text.strip().rstrip('.')
            question_text = p_tag.get_text().replace(p_tag.find('strong').text, '').strip()
            output_result.append(f"{question_number}. {question_text}")
            # out.write(f"{question_number}. {question_text}\n")

            # Extract options (if any)
            options = q_div.find_all('div', class_='option')
            for opt in options:
                label = opt.find('label')
                if label:
                    option_text = label.get_text(strip=True)
                    # out.write(f"{option_text}\n")
                    output_result.append(option_text)
            output_result.append("")
            # out.write("\n")  # Empty line between questions
    final_output = "\n".join(output_result)
    # print(f"✅ Extracted content saved to: {final_output}")
    return final_output
