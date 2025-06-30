from openai import AzureOpenAI

# def load_file_content(file_path):
#     with open(file_path,"r",encoding="utf-8") as f:
#         return f.read()

# json_content = load_file_content(r"C:\CursoryTech POC\TXT-JSON\output_formatted_final.json")
# html_content = load_file_content(r"C:\CursoryTech POC\TXTtoHTML\v2_html.html")
# txt_content = Preprocessing.preprocess.preprocess_txt_file()

# with open (r"C:\CursoryTech POC\Preprocessing\html_preprocess(large).txt","r") as reader:
#     txt_content = reader.read()

def compare_using_model(html_txt_content,json_content):

    client = AzureOpenAI(
        azure_endpoint="https://samue-mc8s7e38-eastus2.openai.azure.com/openai/deployments/gpt-4.1/chat/completions?api-version=2025-01-01-preview",
        api_key="8yZBhA7XmCZqN7RbhhPJfdUce3AxbUtyAQpTre4sjVRZc4WZd4HFJQQJ99BFACHYHv6XJ3w3AAAAACOGr3Hs",
        api_version="2025-01-01-preview"
    )

    deployment_name = "gpt-4.1"


# TEXT FILE COMPARISON

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

At the end, if everything matches exactly (word-for-word), return:
✅ No mismatch found.

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
        max_tokens=1000
    )
    final_output = response.choices[0].message.content
    # print(response.choices[0].message.content)
    final_output = final_output.replace("TXT","HTML")
    return (final_output)

# compare_using_model(txt_content,json_content)