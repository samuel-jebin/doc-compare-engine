from flask import Flask,request,jsonify, render_template
from flask_cors import CORS
from AzureResources import docIntelligence
from AzureResources import blob
from TXTtoHTML import htmlv1
from Preprocessing import preprocess
from ModelComparison import compare
from TXTtoJSON import jsonv1
import uvicorn

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return render_template('index.html')

@app.route("/json_to_blob", methods=['POST'])
def json_to_blob():
    file = request.files.get('file')
    if not file:
        return jsonify({"Error": "No file provided"}), 400

    try:
        file_byte_1 = file.read()
        extracted_text_from_file = docIntelligence.analyze_documents(file_byte_1)
        cleaned_text = htmlv1.preprocess_txt(extracted_text_from_file)
        json_content = jsonv1.convert_txt_json(cleaned_text)
        result = blob.upload_json_to_blob(json_content,"test-json.json")
        
        if result:
            return jsonify({
                "Message":"Upload Successfull "
            }),200
                 
    except Exception as e:
        return jsonify({"message": "Upload failed", "error": str(e)}), 400
 

@app.route('/upload_and_process', methods=['POST'])
def upload_and_process():
    file = request.files.get('file')
    if not file:
        return jsonify({"Error": "No file provided"}), 400
    
    try:
        file_byte = file.read()
        extracted_text_from_file = docIntelligence.analyze_documents(file_byte)
        cleaned_text = htmlv1.preprocess_txt(extracted_text_from_file)
        Html_content = htmlv1.txt_to_html_form(cleaned_text)
        html_to_txt  = preprocess.extract_questions_from_html(Html_content)
        json_content = blob.read_json_from_blob("cursorytech-json","test-json.json")
        
        final_output = compare.compare_using_model(html_to_txt,json_content)
        
        return jsonify({
            "comparison_result" : final_output,
            "html_content":Html_content
        }),200
        
    except Exception as e:
        print(f"error {e}")
        return jsonify({
            "error":str(e)
        }),500
        

  
if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0",port=8000)