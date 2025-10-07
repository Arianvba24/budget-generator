import streamlit as st
from dashboard import dashboard_function
from budget import budget_function
from budget_generator import budget_generator

def page2():
    st.title("Comida gratis")



def main():
    st.set_page_config(layout="wide")
    opcion = st.sidebar.selectbox("Menu",["Presupuestos","Ayuda"])

    if opcion == "Dashboard":
        # dashboard_function()
        pg = st.navigation([st.Page(dashboard_function,title="Base de datos"), st.Page(page2)],position="hidden")
        pg.run()
        
        # st.rerun(scope="app")



    elif opcion == "Presupuestos":

        pg = st.navigation([st.Page(budget_function,title="Base de datos"), st.Page(budget_generator,title="Generador de presupuestos")],position="top")
        pg.run()
        



    elif opcion == "Ayuda":
        st.title("Ayuda")

    


if __name__=="__main__":
    main()