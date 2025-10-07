import fitz  # PyMuPDF
from PIL import Image
import io
import streamlit as st

def image_generator(ruta_pdf):
    # Abrir archivo PDF en modo lectura binaria
    with open(r"C:\Users\Cash\Desktop\proyectos julio\streamlit\valores\tmp\valores - COPIA.pdf", "rb") as f:
        pdf_data = f.read()
    
    doc = fitz.open(stream=pdf_data, filetype="pdf")
    st.write("### Vista previa del presupuesto")

    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))  # Escalado x2
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format="PNG")
        st.image(img_byte_arr.getvalue(), caption=f"Página {page_num + 1}",width=700)

