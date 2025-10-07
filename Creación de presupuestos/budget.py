import streamlit as st
import pandas as pd
import sqlite3
import datetime
import time
from datetime import datetime as dt

meses_del_año = {"Enero" : 1,"Febrero" : 2,"Marzo" : 3,"Abril" : 4,"Mayo" : 5,"Junio" : 6,
"Julio" : 7,"Agosto" : 8,"Septiembre" : 9,"Octubre" : 10,"Noviembre" : 11,"Diciembre" : 12
}


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

def insertar_datos(id_presupuesto:str,cliente:str,obra:str,fecha:datetime.datetime,precio: float,comentarios:str):
    conn = sqlite3.connect(r"C:\Users\Cash\Desktop\proyectos julio\streamlit\Creación de presupuestos\presupuestos.db")
    cursor = conn.cursor()

    try:
        cursor.execute("""
        INSERT INTO presupuestos VALUES(null,?,?,?,?,?,?)
        
        
        """,[id_presupuesto,cliente,obra,fecha,precio,comentarios])

        st.success("Valores insertados con éxito!")

        conn.commit()
        conn.close()


    except Exception as e:
        st.error("No se ha podido introducir el valor")
        print(e)
        conn.commit()
        conn.close()
    


# Dialog function----------------------------------
@st.dialog("Elige la opción")
def dialog_function():
    st.write("¿Desea generar un nuevo mes para los presupuestos? En caso de que si seleccione los valores en el desplegable y dele a Aceptar en caso contrario dele a Salir")

    col1b,col2b = st.columns([1,1])

    with col1b:
        mes_valor = st.selectbox("Mes",["Enero","Febrero","Marzo","Abril","Mayo","Junio","Julio","Agosto","Septiembre","Octubre","Noviembre","Diciembre"])

    with col2b:
        año_valor = st.number_input("Año",value=2020)

    meses_del_año = {"Enero" : 1,"Febrero" : 2,"Marzo" : 3,"Abril" : 4,"Mayo" : 5,"Junio" : 6,
    "Julio" : 7,"Agosto" : 8,"Septiembre" : 9,"Octubre" : 10,"Noviembre" : 11,"Diciembre" : 12
    }
    col1c,col2c = st.columns([1,1])

    with col1c:
        if st.button("Aceptar"):
            st.session_state["mes_valor"] = mes_valor
            st.session_state["año_valor"] = año_valor
            valor = f'ID-{st.session_state["año_valor"]}{meses_del_año[st.session_state["mes_valor"]]:02d}010001'
            st.session_state["nuevo_valor"] = valor
            st.session_state["cambio_valor"] = True
            st.rerun()

    with col2c:
        if st.button("Salir"):
            st.rerun()






    


    



# Modificar presupuestos---------------------------------------------------------------------------------
    # -------------------------------------------------------------------------------------------------------
def query_values(id_value : str):

    try:

        conn = sqlite3.connect(r"C:\Users\Cash\Desktop\proyectos julio\streamlit\Creación de presupuestos\presupuestos.db")
        query = f"""SELECT * FROM presupuestos WHERE "ID_presupuesto" =='{id_value}';"""

        df = pd.read_sql(query,con=conn)

        st.session_state.obra1 = df["Obra"].values[0]
        # print(df["Obra"].values)
        st.session_state.id_presupuesto1 = id_value
        st.session_state.cliente1 = df["Cliente"].values[0]
        date_value = dt.strptime(df["Fecha"].values[0],"%Y-%m-%d")
        # print(type(date_value))
        st.session_state.fecha_presupuesto1 = date_value
        st.session_state.precio1 = float(df["Precio"].values[0])
        st.session_state.comentario1 = df["Comentarios"].values[0]

        conn.commit()
        conn.close()


    except Exception as e:
        conn.commit()
        conn.close()


    except Exception as e:
        pass

# Modificar presupuestos---------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------------
# change_values(cliente,obra,fecha_presupuesto,precio,comentario)
def change_values(id_value,cliente1,obra1,fecha_presupuesto1:datetime.datetime,precio1,comentario1):
    try:

        conn = sqlite3.connect(r"C:\Users\Cash\Desktop\proyectos julio\streamlit\Creación de presupuestos\presupuestos.db")
        cursor = conn.cursor()
        print(type(fecha_presupuesto1))

        # fecha_final = dt.strptime(fecha_presupuesto1,"%Y-%m-%d")

        query = f"""UPDATE presupuestos
        SET "Cliente" = '{cliente1}',"Obra" = '{obra1}',"Fecha" = '{fecha_presupuesto1}',"Precio" = {precio1},"Comentarios" = '{comentario1}'
        WHERE "ID_presupuesto" =='{id_value}';"""

        cursor.execute(query)

        conn.commit()
        conn.close()


    except Exception as e:
        print(e)
        conn.commit()
        conn.close()


        
#Eliminar valores-----------------------------------------------------------------------
#---------------------------------------------------------------------------------------
def delete_values(id_value:str):
    try:

        conn = sqlite3.connect(r"C:\Users\Cash\Desktop\proyectos julio\streamlit\Creación de presupuestos\presupuestos.db")
        cursor = conn.cursor()

        query = f"""

        DELETE 
        FROM presupuestos
        WHERE "ID_presupuesto" == '{id_value}';      

        """
        cursor.execute(query)
        conn.commit()
        conn.close()

    except Exception as e:
        print(e)

        conn.commit()
        conn.close()


@st.dialog("Elija la opción")
def alert_delete_values(id_value:str):
    st.header("¿Esta seguro de que desea borrar el registro de manera permanente?")

    col1d,col2d = st.columns([1,1])

    with col1d:
        if st.button("Si"):
            delete_values(id_value)
            st.success("Registro eliminado con éxito")
            time.sleep(1.5)
            st.rerun()


    with col2d:
        if st.button("No"):
            st.rerun()






def budget_function():
    if "mes_valor" not in st.session_state:
        st.session_state["mes_valor"] = False

    if "año_valor" not in st.session_state:
        st.session_state["año_valor"] = False

    if "nuevo_valor" not in st.session_state:
        st.session_state["nuevo_valor"] = False 
    
    st.title("Presupuestos")
    st.markdown("### Base de datos")
    df = cargar_dataframe()
    last_value = list(df["ID_presupuesto"].values)[-1]

    if "cambio_valor" not in st.session_state:
        st.session_state["cambio_valor"] = False

    if "cambio_valor" in st.session_state:
        if st.session_state["cambio_valor"] == True:
            pass
        else:
            st.session_state["nuevo_valor"] = f'{last_value[:11]}{int(last_value[-1]) + 1:04d}'


   
    st.dataframe(df)
    col1a,col2a = st.columns([3,4])





    with col1a:
        boton1 = st.button("Generar nueva fecha de registro",use_container_width=True)
        if boton1:
            dialog_function()
            # new_value = f'ID-{st.session_state["año_valor"]}{meses_del_año[st.session_state["mes_valor"]]}010001'

            
    # st.write(st.session_state)
    tab1, tab2,tab3 = st.tabs(["Creador de presupuestos","Modificar presupuesto","Eliminar presupuesto"])

    with tab1:
        col1,col2 = st.columns([1,4])
        with col1:
            id_presupuesto = st.text_input("ID presupuesto",value=st.session_state["nuevo_valor"],disabled=True)

        with col2:
            cliente = st.text_input("Cliente")

        col3,col4,col5 = st.columns([3,1,1])

        with col3:
            obra = st.text_input("Obra")
        with col4:
            fecha_presupuesto = st.date_input("Fecha",format="DD/MM/YYYY")
        with col5:
            precio = st.number_input("Precio",value=1.00)

        comentario = st.text_area("Comentarios",value="Sin comentarios")

        if st.button("Insertar valores"):
            insertar_datos(id_presupuesto,cliente,obra,fecha_presupuesto,precio,comentario)
            st.success("Valores insertados con éxito!")
            time.sleep(1.5)
            if "cambio_valor" in st.session_state:
                if st.session_state["cambio_valor"] == True:
                    st.session_state["cambio_valor"] = False
                    st.rerun(scope="app")
            st.rerun()


    

    with tab2:

        df_valores = list(df["ID_presupuesto"].values)

        if "id_presupuesto1" not in st.session_state:
            st.session_state["id_presupuesto1"] = df_valores[0]
            
        col1,col2 = st.columns([1,4])
        with col1:

            id_presupuesto = st.selectbox("ID_presupuesto",df_valores,key="id_presupuesto1", on_change=lambda:query_values(st.session_state["id_presupuesto1"]),index=None)


        with col2:
            cliente = st.text_input("Cliente",key="cliente1")

        col3,col4,col5 = st.columns([3,1,1])

        with col3:
            obra = st.text_input("Obra",key="obra1")
        with col4:
            fecha_presupuesto = st.date_input("Fecha",format="DD/MM/YYYY",key="fecha_presupuesto1")
        with col5:
            precio = st.number_input("Precio",value=1.00,key="precio1")

        comentario = st.text_area("Comentarios",value="Sin comentarios",key="comentario1")

        if st.button("Modificar valores",key=7):
            change_values(id_presupuesto,cliente,obra,fecha_presupuesto,precio,comentario)
            
            st.success("Valores modificados con éxito!")
            time.sleep(1.5)


    with tab3:
        st.header("Seleccione cualquiera de los presupuestos que desea eliminar")
        valor_eliminar = st.selectbox("ID_presupuestos",df_valores,key="id_presupuestos2")
        if st.button("Eliminar valores",key="eliminar_valores"):
            # delete_values(valor_eliminar)
            try:
                alert_delete_values(valor_eliminar)
                

            except Exception as e:
                print(f"Ha habido un error a la hora de eliminar el registro. El error es el siguiente: {e}")

        

        

    
    