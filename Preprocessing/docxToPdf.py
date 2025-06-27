from docx2pdf import convert

def convert_docx_to_pdf(docx_path,out = "conevrted.pdf"):
    convert(docx_path,out)
    
convert_docx_to_pdf(r"C:\Users\K1194\Downloads\SmallProgramming.docx")