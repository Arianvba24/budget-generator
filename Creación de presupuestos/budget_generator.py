import streamlit as st
import pandas as pd
import sqlite3
from st_keyup import st_keyup
from image_generator import image_generator
from datetime import datetime
from docx_generator import docx_generator
import time
from pdf_generator import pdf_generator
from image_generator import image_generator
from file_downloader import FileDownloader

def cargar_dataframe():
    conn = sqlite3.connect(r"C:\Users\Cash\Desktop\proyectos julio\streamlit\Creación de presupuestos\presupuestos.db")
    cursor = conn.cursor()

    try:
        query = """
        SELECT * FROM presupuestos;
        """
        df = pd.read_sql(query,con=conn)
        


        # print(list(df["ID_presupuesto"].values)[-1])

        conn.commit()
        conn.close()

        return df

    except Exception as e:
        print(type(e))
        conn.commit()
        conn.close()



# Funciones dialog---------------------------------------------------------

@st.dialog("Insertar importe")
def value_generator():

    st.write("Escriba el importe que desea que aparezca en el presupuesto")
    valor = st.number_input("Importe",value=100.00)

    col1g,col2g = st.columns([1,1])
    valor_numero = st.button("Insertar datos",use_container_width=True)
    with col1g:
        if valor_numero:
            alerta_boton = True
            st.session_state["Estructura"].append("importe")
            if valor % 1 == 0:
                st.session_state["valores_estructura"].append(str(int(valor)))

            else:
                st.session_state["valores_estructura"].append(str(valor))

        
    try:
        if alerta_boton == True:
            st.success("Valor insertado con éxito!")


    except Exception as e:
        print(e)

    # with col2g:
    #     st.button("Salir",use_container_width=True)
     



@st.dialog("Insertar linea de texto")
def linea_generator():
    st.write("Escriba el texto que desea que aparezca en el presupuesto")
    valor = st.text_input("Texto",key="03415634")

    col1g,col2g = st.columns([1,1])
    with col1g:
        linea_boton = st.button("Insertar texto",use_container_width=True,key="0000001")
        if linea_boton:
            alerta_linea = True
            st.session_state["Estructura"].append("linea")
            st.session_state["valores_estructura"].append(valor)

    if linea_boton:
        st.success("Valor insertado con éxito!")
    # with col2g:
    #     st.button("Salir",use_container_width=True)




@st.dialog("Insertar sub-linea de texto")
def sub_line_generator():
    st.write("Escriba el texto que desea que aparezca como sub-linea")
    valor = st.text_input("Texto",key="03415635")

    col1g,col2g = st.columns([1,1])
    with col1g:
        linea_boton = st.button("Insertar texto",use_container_width=True,key="0000002")
        if linea_boton:
            alerta_linea = True
            st.session_state["Estructura"].append("sub-linea")
            st.session_state["valores_estructura"].append(valor)

    if linea_boton:
        st.success("Valor insertado con éxito!")

@st.dialog("Insertar forma de pago")
def payment_form():
    st.write("Escriba el texto que desea que aparezca como forma de pago")
    valor = st.text_input("Texto",key="03415636")

    col1g,col2g = st.columns([1,1])
    with col1g:
        linea_boton = st.button("Insertar texto",use_container_width=True,key="0000003")
        if linea_boton:
            alerta_linea = True
            st.session_state["Estructura"].append("forma_pago")
            st.session_state["valores_estructura"].append(valor)

    if linea_boton:
        st.success("Valor insertado con éxito!")

#-----------------------------------------------------------------------

def budget_generator():
    if "current_value_state" not in st.session_state:
        st.session_state["current_value_state"] = True


    st.title("Generador de presupuestos")
    df = cargar_dataframe()
    df_1 = df.copy()
    valores_df = list(df["ID_presupuesto"].values)
    col1e,col2e,col3e = st.columns([3,2,3])
    with col1e:
        st.markdown("### Elija el presupuesto el cual desea crear")


    campos_valores = df.columns.to_list()

    with col2e:
        st.selectbox("Elija el campo a filtrar",campos_valores,key="listado_valores")
        

    with col3e:
        with_default = st_keyup("Enter a value", value="", key="campo_dataframe")
        print(with_default)
    
    if "listado_valores" in st.session_state and "campo_dataframe" in st.session_state:

        df[st.session_state["listado_valores"]] = df[st.session_state["listado_valores"]].astype(str)
        
        df = df.loc[df[st.session_state["listado_valores"]].str.contains(str(with_default)) == True]
        
    st.dataframe(df)





    filtro_df = st.selectbox("Valores",valores_df)


    df_final = df_1.loc[df_1["ID_presupuesto"] == filtro_df]

    time_text = df_final["Fecha"].values[0]

    time_value = datetime.strptime(time_text,"%Y-%m-%d")

    new_time = f"{time_value.day}-{int(time_value.month):02d}-{time_value.year}"
    # print(f"{1:02d}")

    pasar_docx = {

        "REF" : df_final["ID_presupuesto"].values[0],
        "Cliente" : df_final["Cliente"].values[0],
        "Obra" : df_final["Obra"].values[0],
        "Fecha" : new_time
    }

    if "Estructura" not in st.session_state:
        st.session_state["Estructura"] = []

    if "valores_estructura" not in st.session_state:
        st.session_state["valores_estructura"] = []


    col1f,col2f = st.columns([1,1])



    with col1f:
        if st.button("Insertar espacio",key="espacio",use_container_width=True):
            st.session_state["Estructura"].append("espacio")
            st.session_state["valores_estructura"].append("")
        if st.button("Insertar linea",key="linea",use_container_width=True,on_click=linea_generator):
            pass
 


        if st.button("Insertar sub-linea",key="sub-linea",use_container_width=True,on_click=sub_line_generator):
            pass
   
    with col2f:
        
        if st.button("Insertar importe",key="importe",use_container_width=True,on_click=value_generator):
            pass


        if st.button("Insertar borde de separación",key="borde de separación",use_container_width=True):
            st.session_state["Estructura"].append("borde_separación")
            st.session_state["valores_estructura"].append("borde separación")

        if st.button("Insertar forma de pago",key="forma de pago",use_container_width=True,on_click=payment_form):
            pass
            # st.session_state["Estructura"].append("forma_pago")
            # st.session_state["valores_estructura"].append("Valor forma pago")
       

    cola,colb = st.columns([1,1])

    with cola:
        st.write(st.session_state["Estructura"])

    with colb:
        st.write(st.session_state["valores_estructura"])


    values_xp = zip(st.session_state["Estructura"],st.session_state["valores_estructura"])

    # st.html("""
    
    # .stMarkdown
    
    # """)

    st.markdown("""
        <hr style="border: none; height: 1px; background-color: black;" />
        """, unsafe_allow_html=True)

    col1g,col2g = st.columns([1,1])

    with col1g:

        if st.button("Actualizar todo",use_container_width=True):
            st.rerun()

        generar_presupuesto = st.button("Generar presupuesto",use_container_width=True)
        if generar_presupuesto:
            
            try:
                ruta = r"C:\Users\Cash\Desktop\proyectos julio\streamlit\Creación de presupuestos\budget files\valores - COPIA.docx"
                ruta_pdf = r"C:\Users\Cash\Desktop\proyectos julio\streamlit\valores\tmp\valores - COPIA.pdf"
                doc = docx_generator(pasar_docx["REF"],pasar_docx["Cliente"],pasar_docx["Obra"],pasar_docx["Fecha"],*values_xp)
                doc.save(ruta)
                pdf_generator(ruta)
                image_generator(ruta_pdf)

                
                
            except Exception as e:
                st.error("Error")
                print(e)

        

    with col2g:

        if st.button("Borrar registro de lineas",use_container_width=True):
            st.session_state["Estructura"] = []
            st.session_state["valores_estructura"] = []
            st.rerun()

        
        st.write("")
        st.write("")
        st.write("")

        if generar_presupuesto:
            with open(ruta_pdf, "rb") as f:
                pdf_bytes = f.read()

            fd = FileDownloader(pdf_bytes, filename="presupuesto", file_ext="pdf")
            fd.download_pdf()

    

        
    

    # valor = [{"a" : 1}]

    # print(list(valor[0].keys())[0])




    
