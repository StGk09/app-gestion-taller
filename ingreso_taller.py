import streamlit as st
import pandas as pd
import os
from datetime import datetime
from streamlit_drawable_canvas import st_canvas
from PIL import Image
import numpy as np

# --- Configuración Inicial ---
st.set_page_config(page_title="SecondeLife", layout="wide")

# Carpetas de almacenamiento
FOLDERS = ['datos', 'datos/fotos_dispositivos', 'datos/firmas']
for folder in FOLDERS:
    if not os.path.exists(folder):
        os.makedirs(folder)

FILE_PATH = 'datos/registro_reparaciones.csv'

# --- Título y Estilo ---
st.title("🛠️ Sistema de Ingreso - Servicio Técnico")
st.markdown("---")

# --- Función para guardar firmas ---
def guardar_firma(canvas_result, nombre_archivo):
    if canvas_result.image_data is not None:
        # Convertir array de numpy a imagen
        img_data = canvas_result.image_data.astype('uint8')
        # Verificar si el lienzo no está vacío (si es todo transparente/blanco no guardaríamos nada idealmente, 
        # pero aquí guardamos lo que haya si se envió el form)
        img = Image.fromarray(img_data)
        path = os.path.join("datos/firmas", nombre_archivo)
        img.save(path)
        return nombre_archivo
    return None

# --- FORMULARIO PRINCIPAL ---
with st.form("entry_form", clear_on_submit=True):
    
    # SECCIÓN 1: DATOS GENERALES
    st.subheader("1. Datos del Cliente y Dispositivo")
    c1, c2, c3 = st.columns(3)
    with c1:
        cliente = st.text_input("Nombre del Cliente")
        telefono = st.text_input("Teléfono / WhatsApp")
    with c2:
        marca = st.text_input("Marca")
        modelo = st.text_input("Modelo")
    with c3:
        serie = st.text_input("Número de Serie / IMEI")
        clave = st.text_input("Contraseña/Patrón (Opcional)")

    # SECCIÓN 2: ESTADO Y DAÑO
    st.subheader("2. Diagnóstico Inicial")
    dano = st.text_area("Descripción del problema / Daño", height=100)
    
    col_foto, col_cosmetico = st.columns([1, 2])
    with col_foto:
        st.write("📸 **Foto del Dispositivo**")
        input_camara = st.camera_input("Tomar foto")
        input_archivo = st.file_uploader("O subir imagen", type=['png', 'jpg', 'jpeg'])
    
    with col_cosmetico:
        st.write("📋 **Estado Cosmético** (Marcar lo que aplique)")
        cosmetico = st.multiselect(
            "Detalles visuales:",
            ["Pantalla Rayada", "Pantalla Rota", "Golpes en bordes", "Tapa trasera rota", "Botones hundidos", "Sin bandeja SIM", "Mojado"],
            default=[]
        )
        observaciones_cosmeticas = st.text_input("Otras observaciones cosméticas")

    st.markdown("---")

    # SECCIÓN 3: GARANTÍA
    st.subheader("3. Términos de Garantía")
    col_garantia1, col_garantia2 = st.columns(2)
    with col_garantia1:
        tiempo_garantia = st.selectbox("Tiempo de Garantía Estimado", ["Sin Garantía", "15 Días", "30 Días", "3 Meses", "6 Meses"])
    with col_garantia2:
        condiciones = st.text_area("Condiciones Específicas", 
                                   value="La garantía cubre solo la mano de obra y las piezas reemplazadas. No cubre daños por agua o golpes posteriores.",
                                   height=100)

    st.markdown("---")

    # SECCIÓN 4: FIRMAS
    st.subheader("4. Aceptación y Firmas")
    col_firma_cliente, col_firma_tienda = st.columns(2)

    # Configuración común para los lienzos de firma
    canvas_height = 150
    canvas_width = 400
    
    with col_firma_cliente:
        st.write("✍️ **Firma del Cliente**")
        st.caption("Acepto los términos y condiciones anteriores.")
        firma_cliente = st_canvas(
            stroke_width=2,
            stroke_color="#000000",
            background_color="#EEEEEE",
            height=canvas_height,
            width=canvas_width,
            key="canvas_cliente",
        )

    with col_firma_tienda:
        st.write("✍️ **Firma del Recibido (Taller)**")
        st.caption("Confirmación de recepción del equipo.")
        firma_tienda = st_canvas(
            stroke_width=2,
            stroke_color="#0000AA",
            background_color="#EEEEEE",
            height=canvas_height,
            width=canvas_width,
            key="canvas_tienda",
        )

    # BOTÓN FINAL
    enviar = st.form_submit_button("💾 GUARDAR REGISTRO", type="primary")

    if enviar:
        if not cliente or not modelo:
            st.error("⚠️ Faltan datos obligatorios (Nombre o Modelo).")
        else:
            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            # 1. Guardar Foto Dispositivo
            foto_filename = "N/A"
            img_source = input_camara if input_camara else input_archivo
            if img_source:
                foto_filename = f"DEV_{ts}_{cliente}_{modelo}.jpg".replace(" ", "_")
                with open(os.path.join("datos/fotos_dispositivos", foto_filename), "wb") as f:
                    f.write(img_source.getbuffer())

            # 2. Guardar Firmas
            firma_cli_name = f"SIG_CLI_{ts}.png"
            firma_tie_name = f"SIG_SHOP_{ts}.png"
            
            # Guardamos las imágenes de las firmas
            guardar_firma(firma_cliente, firma_cli_name)
            guardar_firma(firma_tienda, firma_tie_name)

            # 3. Guardar Datos en CSV
            nuevo_registro = {
                "Fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Cliente": cliente,
                "Teléfono": telefono,
                "Equipo": f"{marca} {modelo}",
                "Serie/IMEI": serie,
                "Daño": dano,
                "Estado Cosmético": ", ".join(cosmetico) + f" ({observaciones_cosmeticas})",
                "Garantía": tiempo_garantia,
                "Condiciones": condiciones,
                "Foto Dispositivo": foto_filename,
                "Firma Cliente": firma_cli_name,
                "Firma Taller": firma_tie_name
            }

            df_new = pd.DataFrame([nuevo_registro])
            
            if os.path.exists(FILE_PATH):
                df_new.to_csv(FILE_PATH, mode='a', header=False, index=False)
            else:
                df_new.to_csv(FILE_PATH, mode='w', header=True, index=False)

            st.success("✅ ¡Orden de servicio creada exitosamente!")

            st.balloons()

