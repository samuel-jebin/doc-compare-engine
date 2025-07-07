from openai import AzureOpenAI
import json
from bs4 import BeautifulSoup

def summarize_mismatches(mismatch_data):
    if isinstance(mismatch_data, str):
        try:
            mismatch_data = json.loads(mismatch_data)
        except json.JSONDecodeError as e:
            return f"Failed to parse JSON: {str(e)}"

    mismatches = mismatch_data.get("mismatches", [])
    status = mismatch_data.get("summary", {}).get("status", "")

    if not mismatches and "No mismatches found" in status:
        return "No mismatches found"

    summary_lines = []
    for mismatch in mismatches:
        question_number = mismatch.get("questionNumber", "Unknown")
        for issue in mismatch.get("issues", []):
            issue_type = issue.get("type", "Unknown")
            option = issue.get("option", "N/A")
            json_val = issue.get("json", "None")
            html_val = issue.get("html", "None")

            # if issue_type == "Option Mismatch":
            #     summary_lines.append(
            #     f"Option Mismatch on {question_number} (Option {option}):\n"
            #     f"JSON → '{json_val}',\nHTML → '{html_val}'\n"
            # )
            # elif issue_type == "Missing Option":
            #     summary_lines.append(
            #     f"Missing Option on {question_number} (Option {option}):\n"
            #     f"JSON → '{json_val}',\nHTML → '{html_val}'\n"
            # )
            # elif issue_type == "Extra Option in HTML":
            #     summary_lines.append(
            #     f"Extra Option in HTML on {question_number} (Option {option}):\n"
            #     f"JSON → '{json_val}',\nHTML → '{html_val}'\n"
            # )
            # elif issue_type == "Missing Question":
            #     summary_lines.append(
            #     f"Missing Question on {question_number} (Option {option}):\n"
            #     f"JSON → '{json_val}',\nHTML → '{html_val}'\n"
            # )
                
            summary_lines.append(
                f"{issue_type} on {question_number} (Options {option}):\n"
                f"JSON -> '{json_val}',\n"
                f"HTML -> '{html_val}'\n"
            )

    final_summary = "\n".join(summary_lines)
    return final_summary


def compare_using_model(html_txt_content,json_content):

    client = AzureOpenAI(
        azure_endpoint="https://samue-mc8s7e38-eastus2.openai.azure.com/openai/deployments/gpt-4.1/chat/completions?api-version=2025-01-01-preview",
        api_key="8yZBhA7XmCZqN7RbhhPJfdUce3AxbUtyAQpTre4sjVRZc4WZd4HFJQQJ99BFACHYHv6XJ3w3AAAAACOGr3Hs",
        api_version="2025-01-01-preview"
    )

    deployment_name = "gpt-4.1"

    system_message = {
        "role": "system",
        "content": (
            "You are a strict document comparison engine.\n"
            "You will receive two versions of a questionnaire: one in JSON (source of truth) and one extracted from HTML content.\n\n"
            "Instructions:\n"
            "- JSON is the source of truth.\n"
            "- Ignore the 'questionId' field.\n"
            "- Match questions by 'questionNumber' (e.g., S1, Q2).\n"
            "- When comparing 'questionContent' and 'options', follow these rules:\n"
            "  - Match by exact words — do NOT rely on semantic similarity.\n"
            "  - If any word is missing, added, misspelled, or jumbled: flag it.\n"
            "  - Check for number mismatches in both question and options.\n"
            "- Ignore formatting differences such as:\n"
            "  - Extra/missing whitespace (spaces, tabs)\n"
            "  - Newlines or line breaks\n"
            "  - Case differences (e.g., 'Yes' vs 'yes')\n"
            "  - Punctuation (periods, commas)\n"
            "- Do NOT list any question unless there's a **clear word-level mismatch**.\n"
            "- At the end, if all questions match exactly, return:\n"
            "✅ No mismatch found."
        )
    }

    user_prompt = {
    "role": "user",
    "content": f"""
You will now compare two versions of a form. The JSON version is the source of truth. The TXT version may contain formatting issues or typing mistakes.

Compare them **question-by-question** using the `questionNumber`.

Match text by **exact words only** — semantic similarity is not allowed.

Flag mismatches when:
- Words are misspelled, jumbled, added, or missing
- Numbers in questions or options do not match
- Options are missing, duplicated, or changed

Ignore:
- Whitespace differences (extra/missing spaces, tabs)
- Line breaks
- Case (uppercase/lowercase)
- Punctuation (periods, commas)

Do not report anything unless there is a **clear word mismatch**.

✅ At the end of your analysis, return the result as a **JSON object** with the following structure:

{{
  "mismatches": [
    {{
      "questionNumber": "Q1",
      "issues": [
        {{
          "type": "Option Mismatch",
          "option": "A",
          "json": "Correct option from JSON",
          "html": "Incorrect or mismatched option from HTML"
        }}
      ]
    }}
  ],
  "summary": {{
    "total_questions_checked": 10,
    "questions_with_mismatches": 2,
    "mismatch_types": {{
      "Option Mismatch": 5,
      "Missing Option": 1,
      "Missing Question": 1,
      "Extra Option in HTML": 1
    }},
    "status": "✅ No mismatches found" OR "❌ Mismatches found"
  }}
  
}}

--- JSON ---
{json_content}

--- Extracted from HTML ---
{html_txt_content}
"""
}

    response = client.chat.completions.create(
        model = deployment_name,
        messages=[system_message,user_prompt],
        temperature=0.0,
        top_p=1.0,
        max_tokens=800
    )
    final_output = response.choices[0].message.content
    final_output = final_output.replace("TXT","HTML")
    return (final_output)


def highlight_html_mismatch(html_content, json_content):
    
    soup  = BeautifulSoup(html_content,'html.parser')
    
    mismatched_data = json.loads(json_content)
    mismatches = mismatched_data.get("mismatches",[])
    
    for question in mismatches:
        question_number = question.get("questionNumber", "").strip().rstrip(".")

        for issue in question.get("issues", []):
            option = issue.get("option")
            html_option_text = issue.get("html")

            if not html_option_text:
                continue

            expected_id = f"{question_number}_{option}".upper()

            label = soup.find("label", attrs={"for": expected_id})
            if label:
                label.clear()

                highlight_span = soup.new_tag("span")
                highlight_span["style"] = "background-color: yellow"
                highlight_span.string = html_option_text

                label.append(highlight_span)
            else:
                print(f"⚠️ Warning: No label found for ID '{expected_id}'")
    
    return str(soup)


# def load_file_content(file_path):
#     with open(file_path,"r",encoding="utf-8") as f:
#         return f.read()

# model_result = load_file_content(r"C:\CursoryTech POC\ModelComparison\modelResult.txt")
# json_content = load_file_content(r"C:\CursoryTech POC\TXTtoJSON\v2_output.json")
# html_content = load_file_content(r"C:\CursoryTech POC\TXTtoHTML\v2_html.html")
# txt_content = Preprocessing.preprocess.preprocess_txt_file()

# with open (r"C:\CursoryTech POC\Preprocessing\html_preprocess(large).txt","r") as reader:
#     txt_content = reader.read()

# res = summarize_mismatches(model_result)
# print(res)