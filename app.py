import streamlit as st
import hashlib

# --- CONFIGURACIÓN ---
ALFABETO = "abcdefghijklmnñopqrstuvwxyz"

def obtener_llave(palabra_secreta):
    # Genera una llave de 64 caracteres hex que actúa como semilla
    return hashlib.sha256(palabra_secreta.encode()).hexdigest()

def cifrar(mensaje, clave_secreta):
    clave = obtener_llave(clave_secreta)
    resultado = ""
    # Limpiamos el mensaje: quitamos espacios y dejamos solo letras
    mensaje = "".join([c for c in mensaje.lower() if c in ALFABETO])
    
    for i in range(len(mensaje)):
        m_idx = ALFABETO.index(mensaje[i])
        k_idx = int(clave[i % len(clave)], 16) % 27
        resultado += ALFABETO[(m_idx + k_idx) % 27]
    return resultado

def descifrar(mensaje_cifrado, clave_secreta):
    clave = obtener_llave(clave_secreta)
    resultado = ""
    for i in range(len(mensaje_cifrado)):
        c_idx = ALFABETO.index(mensaje_cifrado[i].lower())
        k_idx = int(clave[i % len(clave)], 16) % 27
        # Restamos la clave y usamos el módulo para volver al valor original
        resultado += ALFABETO[(c_idx - k_idx) % 27]
    return resultado

# --- INTERFAZ WEB (STREAMLIT) ---
st.title("🛡️ Máquina Enigma Profesional")
st.subheader("Cifrado basado en Base27 y SHA-256")

clave_input = st.text_input("Introduce tu palabra secreta:", type="password")

col1, col2 = st.columns(2)

with col1:
    msg_cifrar = st.text_area("Mensaje a cifrar:")
    if st.button("Cifrar"):
        if clave_input and msg_cifrar:
            st.success(f"Resultado: {cifrar(msg_cifrar, clave_input)}")
        else:
            st.warning("Completa todos los campos.")

with col2:
    msg_descifrar = st.text_area("Mensaje a descifrar:")
    if st.button("Descifrar"):
        if clave_input and msg_descifrar:
            st.info(f"Mensaje original: {descifrar(msg_descifrar, clave_input)}")
        else:
            st.warning("Completa todos los campos.")
