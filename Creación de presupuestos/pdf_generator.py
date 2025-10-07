import os
import subprocess
import streamlit as st


def pdf_generator(ruta):

    docx_path = ruta
    output_dir = r"C:\Users\Cash\Desktop\proyectos julio\streamlit\valores\tmp"
    final_pdf = r"C:\Users\Cash\Desktop\proyectos julio\streamlit\valores\output.pdf"


    subprocess.run([
        r"C:\Program Files\LibreOffice\program\soffice.exe", 
        "--headless",
        "--convert-to", "pdf",
        "--outdir", output_dir,
        docx_path
    ], check=True)

    print("Archivo convertido antes")
    converted_pdf = os.path.join(output_dir, r"C:\Users\Cash\Desktop\proyectos julio\streamlit\valores\valores.pdf")
    # os.rename(converted_pdf, final_pdf)
