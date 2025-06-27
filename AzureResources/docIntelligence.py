from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential
from dotenv import load_dotenv
import os


def analyze_documents(file_byte):
    load_dotenv()
    endpoint = "https://cursorydocanalyzer.cognitiveservices.azure.com/"
    key = "4oLPogAk5pcBlSaEsyle2qOO6qW0JETRJ6fwXRq5FS1mIVAU2sBeJQQJ99BFACYeBjFXJ3w3AAALACOGz5j0"
    
    # client = DocumentAnalysisClient(
    #     endpoint=os.getenv('DOC_ENDPOINT'),
    #     credential=AzureKeyCredential(os.getenv("DOC_API")) 
    # )
    client = DocumentAnalysisClient(
        endpoint=endpoint,
        credential=AzureKeyCredential(key) 
    )
    poller = client.begin_analyze_document(
        model_id="prebuilt-document",
        document=file_byte
    )
    result = poller.result()
    lines_output = []
    for page in result.pages:
        for line in page.lines:
            lines_output.append(line.content)
    final_result = "\n".join(lines_output)
    
    return final_result

# def analyze_documents_test(file_path):
#     load_dotenv()
#     endpoint = "https://cursorydocanalyzer.cognitiveservices.azure.com/"
#     key = "4oLPogAk5pcBlSaEsyle2qOO6qW0JETRJ6fwXRq5FS1mIVAU2sBeJQQJ99BFACYeBjFXJ3w3AAALACOGz5j0"
    
    
#     # client = DocumentAnalysisClient(
#     #     endpoint=os.getenv('DOC_ENDPOINT'),
#     #     credential=AzureKeyCredential(os.getenv("DOC_API")) 
#     # )
#     client = DocumentAnalysisClient(
#         endpoint=endpoint,
#         credential=AzureKeyCredential(key) 
#     )
    
    
#     with open(file_path, "rb") as document:
#         poller = client.begin_analyze_document(
#             model_id="prebuilt-document",
#             document=document
#         )
#         result = poller.result()
#     lines_output = []
#     print("\n-- Extracted Content --")
#     for page in result.pages:
#         for line in page.lines:
#             lines_output.append(line.content)
#     temp = "\n".join(lines_output)
            
#     print(temp)
#     with open("output_result","w",encoding="utf-8") as file_writer:
#         file_writer.write(temp)


# analyze_documents_test(r"C:\CursoryTech POC\SmallProgramming.pdf")