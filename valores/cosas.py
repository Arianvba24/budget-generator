import os
import subprocess
import streamlit as st


def pdf_generator():
    docx_path = r"C:\Users\Cash\Downloads\valores.docx"
    output_dir = r"C:\Users\Cash\Desktop\proyectos julio\streamlit\valores\tmp"
    final_pdf = r"C:\Users\Cash\Desktop\proyectos julio\streamlit\valores\output.pdf"


    subprocess.run([
        r"C:\Program Files\LibreOffice\program\soffice.exe", 
        "--headless",
        "--convert-to", "pdf",
        "--outdir", output_dir,
        docx_path
    ], check=True)


    converted_pdf = os.path.join(output_dir, r"C:\Users\Cash\Desktop\proyectos julio\streamlit\valores\valores.pdf")
# os.rename(converted_pdf, final_pdf)
