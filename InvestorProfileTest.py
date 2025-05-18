import streamlit as st

# Configuración inicial
st.title("Asesor de Portafolios Personalizados")
st.header("📋 Completa tu perfil de inversor")

with st.form("Perfil del Inversor"):
    # Preguntas clave
    edad = st.number_input("Edad del inversor:", min_value=18, max_value=100, value=35)
    años_jubilacion = st.number_input("Años hasta la jubilación:", min_value=1, max_value=50, value=30)
    tolerancia_riesgo = st.selectbox("Tolerancia a pérdidas:", ["Baja", "Media", "Alta"], index=2)
    objetivo = st.selectbox("Objetivo principal:", 
                          ["Protección inflación", "Crecimiento", "Ingresos", "Estabilidad"], 
                          index=1)
    horizonte = st.radio("Horizonte de inversión:", 
                       ["Corto plazo [1-3 años]", "Mediano [3-5]", "Largo [5+]"], 
                       index=2)
    liquidez = st.radio("Preferencia por liquidez:", ["Sí", "No"], index=1)
    exposicion_extranjera = st.radio("Exposición a mercados extranjeros:", ["Sí", "No"], index=0)
    
    submitted = st.form_submit_button("Generar Portafolio")

if submitted:
    # Procesar respuestas
    respuestas_usuario = {
        "edad": edad,
        "años_jubilacion": años_jubilacion,
        "tolerancia_riesgo": tolerancia_riesgo,
        "objetivo": objetivo,
        "horizonte": horizonte.split()[0],
        "liquidez": liquidez,
        "exposicion_extranjera": exposicion_extranjera
    }

    # Clasificar perfil
    def clasificar_perfil(respuestas):
        if respuestas["tolerancia_riesgo"] == "Baja" and respuestas["horizonte"] == "Corto":
            return "Conservador"
        elif respuestas["tolerancia_riesgo"] == "Alta" and respuestas["horizonte"] == "Largo":
            return "Agresivo"
        else:
            return "Moderado"
    
    perfil = clasificar_perfil(respuestas_usuario)
    
    # --- CÓDIGO FALTANTE ---
    objetivos_activos = {
        "Protección inflación": ["R. Variable Mercados Emergentes", "Valores Indexados a Inflación", "Activos Reales"],
        "Crecimiento": ["R. Variable EE.UU.", "Capital Privado", "Fondos de Cobertura"],
        "Ingresos": ["R. Fija EE.UU.", "Deuda Corto Plazo", "REITs"],
        "Estabilidad": ["Efectivo/Equivalentes", "Deuda Países Desarrollados"]
    }
    
    data_mercado = {
        "R. Variable EE.UU.": {"rendimiento_anual": 8.5, "volatilidad": 15},
        "R. Fija EE.UU.": {"rendimiento_anual": 4.2, "volatilidad": 5},
        "Valores Indexados a Inflación": {"rendimiento_anual": 6.0, "volatilidad": 7}
    }
    
    activos_recomendados = objetivos_activos.get(respuestas_usuario["objetivo"], [])
    
    def ajustar_por_mercado(activos, perfil):
        if perfil == "Agresivo":
            return sorted(activos, key=lambda x: data_mercado.get(x, {}).get("rendimiento_anual", 0), reverse=True)
        else:
            return sorted(activos, key=lambda x: data_mercado.get(x, {}).get("volatilidad", 100))
    
    activos_ajustados = ajustar_por_mercado(activos_recomendados, perfil)
    
    asignaciones = {
        "Conservador": {"Renta Fija": 70, "Renta Variable": 20, "Alternativos": 10},
        "Moderado": {"Renta Fija": 50, "Renta Variable": 40, "Alternativos": 10},
        "Agresivo": {"Renta Fija": 20, "Renta Variable": 60, "Alternativos": 20}
    }
    
    def generar_portafolio(perfil, activos_ajustados):
        portafolio = asignaciones[perfil].copy()
        if "R. Variable Mercados Emergentes" in activos_ajustados:
            portafolio["Renta Variable"] += 10
            portafolio["Renta Fija"] -= 10
        return portafolio
    
    portafolio_final = generar_portafolio(perfil, activos_ajustados)
    # --- FIN CÓDIGO FALTANTE ---
    
    # Mostrar resultados
    st.success("✅ Análisis completado")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("📊 Asignación por clase")
        st.write(f"- Renta Fija: {portafolio_final['Renta Fija']}%")
        st.write(f"- Renta Variable: {portafolio_final['Renta Variable']}%")
        st.write(f"- Alternativos: {portafolio_final['Alternativos']}%")
    
    with col2:
        st.subheader("📦 Activos recomendados")
        for activo in activos_ajustados:
            st.write(f"- {activo}")

st.markdown("""
**Descargo de responsabilidad**:  
*Esta herramienta no constituye asesoramiento financiero. Los resultados son ilustrativos y no garantizan rendimientos.  
Consulte a un profesional certificado antes de tomar decisiones de inversión.*
""")
