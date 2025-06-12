import streamlit as st
import groq

#Tener nuestros modelos de IA
MODELOS = ['llama3-8b-8192', 'llama3-70b-8192']

#Configuración de la página
def configurar_pagina():
    st.set_page_config(
        page_title="Mi primera pagina con python",
        page_icon="🤓"
    )
    st.title("Bienvenidos a mi chatbot 🤖")

#Mostrar el sidebar con los modelos
def mostrar_sidebar():
    st.sidebar.title("Elegi tu modelo de chatbot")
    modelo=st.sidebar.selectbox( 
        "Selecciona un modelo",
        MODELOS,
        index=0
    )   #Crea un selectbox en la barra lateral para elegir el modelo
    st.write("Elegiste el modelo:", modelo)
    return modelo

# un cliente de Groq
def crear_cliente_groq():
    groq_api_key = st.secrets["GROQ_API_KEY"] #Almacena la clave de la API de Groq
    return groq.Groq(api_key=groq_api_key) #Crea un cliente de Groq con la clave de la API

#Inicializa el estado de los mensajes del chat
def inicializacion_estado_chat():
    if "mensajes" not in st.session_state:
        st.session_state.mensajes = []

#historial de chat
def mostrar_historial_chat():
    for mensaje in st.session_state.mensajes:
        with st.chat_message(mensaje["role"]): #Context manager
            st.markdown(mensaje["content"])

#Obtiene el mensaje del usuario
def obtener_mensaje_usuario():
    return st.chat_input("Escribe tu mensaje acá...") #Entrada de chat para el usuario

def agregar_mensaje_al_historial(role, content):
    st.session_state.mensajes.append({"role": role, "content": content}) #Agrega un mensaje al historial del chat

#Mostrar los mensajes en pantalla
def mostrar_mensajes(role, content):
    with st.chat_message(role): #Context manager para mostrar el mensaje
        st.markdown(content) #Muestra el contenido del mensaje

#Llamar al modelo de Groq
def obtener_respuesta_modelo(cliente, modelo, mensajes):
    respuesta=cliente.chat.completions.create(
        model=modelo, #Modelo a usar
        messages=mensajes,
        stream=False
        )
    return respuesta.choices[0].message.content #Devuelve el contenido de la respuesta del modelo

def ejecutar_app():
    configurar_pagina(); #Configura la página de Streamlit
    modelo= mostrar_sidebar() #Muestra el sidebar con los modelos
    cliente= crear_cliente_groq() #Crea un cliente de Groq
    inicializacion_estado_chat() #Inicializa el estado del chat
    mostrar_historial_chat() #Muestra el historial del chat
    mensaje_usuario=obtener_mensaje_usuario() #Obtiene el mensaje del usuario
    
    if mensaje_usuario:
        #Agregar el mensaje del usuario al historial y mostrarlo
        agregar_mensaje_al_historial("user", mensaje_usuario)
        mostrar_mensajes("user", mensaje_usuario)
        # Obtener respuesta de la IA y mostrarla
        respuesta = obtener_respuesta_modelo(cliente, modelo, st.session_state.mensajes)
        agregar_mensaje_al_historial("assistant", respuesta)
        mostrar_mensajes("assistant", respuesta)


if __name__ == "__main__": #Si este es el archivo principal, entonces ejecuta la app
    ejecutar_app()