import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px

# Configuración inicial de la página
st.set_page_config(page_title="Asesor Financiero Inteligente", layout="wide")

# Título principal
st.title("💰 Asesor Financiero Inteligente")
st.header("Herramienta Completa de Planificación de Inversiones")

# Inicializar variables de estado
if 'perfil' not in st.session_state:
    st.session_state.perfil = None
if 'asignacion' not in st.session_state:
    st.session_state.asignacion = None

# --- SECCIÓN DE FORMULARIO PRINCIPAL ---
with st.form("Formulario_Inversor"):
    # SECCIÓN 1: PERFIL DEMOGRÁFICO
    with st.expander("👤 Información Personal Básica", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            edad = st.number_input("1. Edad actual:", min_value=18, max_value=100, value=35)
            pais = st.selectbox("2. País de residencia:", ["España", "México", "Colombia", "Argentina", "Otro"])
        with col2:
            años_jubilacion = st.number_input("3. Años hasta la jubilación:", min_value=0, max_value=50, value=20)
            dependientes = st.number_input("4. Personas dependientes:", min_value=0, max_value=10, value=0)

    # SECCIÓN 2: SITUACIÓN FINANCIERA
    with st.expander("💼 Situación Económica Actual", expanded=False):
        col3, col4 = st.columns(2)
        with col3:
            patrimonio = st.number_input("5. Patrimonio neto actual (USD):", min_value=0, value=150000)
            ingresos_mensuales = st.number_input("6. Ingresos mensuales netos (USD):", min_value=0, value=5000)
        with col4:
            deudas = st.number_input("7. Deudas totales (USD):", min_value=0, value=30000)
            gastos_mensuales = st.number_input("8. Gastos mensuales promedio (USD):", min_value=0, value=3000)

    # SECCIÓN 3: OBJETIVOS Y TOLERANCIA AL RIESGO
    with st.expander("🎯 Objetivos de Inversión", expanded=False):
        col5, col6 = st.columns(2)
        with col5:
            objetivo_principal = st.selectbox("9. Objetivo principal:", 
                ["Preservar capital", "Generar ingresos", "Crecimiento moderado", "Crecimiento agresivo"])
            horizonte = st.radio("10. Horizonte temporal:", 
                ["Corto plazo (1-3 años)", "Mediano plazo (3-5 años)", "Largo plazo (+5 años)"], index=2)
        with col6:
            riesgo_tolerancia = st.select_slider("11. Tolerancia al riesgo:", 
                options=["Mínima", "Baja", "Moderada", "Alta", "Máxima"], value="Moderada")
            liquidez_necesaria = st.slider("12. Necesidad de liquidez:", 0, 100, 30)

    # SECCIÓN 4: ESTRATEGIA DE INVERSIÓN
    with st.expander("📈 Estrategia de Inversión", expanded=False):
        col7, col8 = st.columns(2)
        with col7:
            conocimiento_mercados = st.selectbox("13. Conocimiento de mercados:", 
                ["Principiante", "Intermedio", "Avanzado"])
            frecuencia_operaciones = st.radio("14. Frecuencia de operaciones:", 
                ["Pasiva (buy & hold)", "Ocasional", "Activa"])
        with col8:
            exposicion_internacional = st.radio("15. Exposición internacional:", ["Sí", "No"], index=0)
            etica_ambiental = st.checkbox("16. Preferencia por inversiones sostenibles")

    submitted = st.form_submit_button("🚀 Generar Plan de Inversión")

# --- PROCESAMIENTO DE DATOS ---
if submitted:
    # 1. Determinación del perfil de riesgo
    def clasificar_perfil(edad, riesgo, horizonte):
        edad_factor = max(0, (100 - edad) / 10)
        riesgo_val = {"Mínima": 1, "Baja": 2, "Moderada": 3, "Alta": 4, "Máxima": 5}[riesgo]
        horizonte_val = {"Corto plazo (1-3 años)": 1, "Mediano plazo (3-5 años)": 2, "Largo plazo (+5 años)": 3}[horizonte]
        
        puntaje_total = (edad_factor * 0.3) + (riesgo_val * 0.4) + (horizonte_val * 0.3)
        
        if puntaje_total < 2.0:
            return "Conservador"
        elif puntaje_total < 3.5:
            return "Moderado"
        else:
            return "Agresivo"

    st.session_state.perfil = clasificar_perfil(edad, riesgo_tolerancia, horizonte)
    
    # 2. Asignación de activos según perfil
    matriz_activos = {
        "Conservador": {"Renta Fija": 70, "Renta Variable": 20, "Alternativos": 10},
        "Moderado": {"Renta Fija": 50, "Renta Variable": 40, "Alternativos": 10},
        "Agresivo": {"Renta Fija": 20, "Renta Variable": 60, "Alternativos": 20}
    }
    
    # 3. Ajustes por objetivos específicos
    asignacion_base = matriz_activos[st.session_state.perfil].copy()
    
    if objetivo_principal == "Crecimiento agresivo":
        asignacion_base["Renta Variable"] += 10
        asignacion_base["Renta Fija"] -= 10
    elif objetivo_principal == "Preservar capital":
        asignacion_base["Renta Fija"] += 15
        asignacion_base["Alternativos"] -= 5
        asignacion_base["Renta Variable"] -= 10
    
    # Normalizar porcentajes
    total = sum(asignacion_base.values())
    asignacion_final = {k: round(v * 100 / total, 1) for k, v in asignacion_base.items()}
    
    st.session_state.asignacion = asignacion_final

# --- SECCIÓN DE RESULTADOS ---
if st.session_state.asignacion:
    st.success("✅ Análisis completado con éxito!")
    
    with st.expander("📊 Perfil de Inversión y Asignación", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Perfil Detectado")
            st.metric("Categoría", st.session_state.perfil)
            st.write(f"**Edad:** {edad} años")
            st.write(f"**Horizonte:** {horizonte}")
            st.write(f"**Tolerancia al riesgo:** {riesgo_tolerancia}")
        
        with col2:
            st.subheader("Asignación de Activos")
            st.metric("Renta Fija", f"{st.session_state.asignacion['Renta Fija']}%")
            st.metric("Renta Variable", f"{st.session_state.asignacion['Renta Variable']}%")
            st.metric("Alternativos", f"{st.session_state.asignacion['Alternativos']}%")

    # --- SIMULADOR DE INVERSIÓN ---
    with st.expander("📈 Simulador de Proyección", expanded=True):
        st.subheader("Configuración de la Simulación")
        
        col_s1, col_s2, col_s3 = st.columns(3)
        with col_s1:
            capital_inicial = st.number_input("Capital inicial (USD):", min_value=0, value=25000)
            aporte_mensual = st.number_input("Aporte mensual (USD):", min_value=0, value=500)
        with col_s2:
            años = st.slider("Período de inversión (años):", 1, 40, 15)
            inflacion = st.slider("Inflación estimada (% anual):", 0.0, 15.0, 3.5)
        with col_s3:
            estrategia = st.radio("Estrategia:", ["DCA (Aportes periódicos)", "Inversión inicial"])
            crecimiento_aportes = st.slider("Crecimiento anual de aportes (%):", 0.0, 20.0, 2.5)

        # Cálculo de proyección
        tasas = {
            "Renta Fija": 0.045 - inflacion/100,
            "Renta Variable": 0.085 - inflacion/100,
            "Alternativos": 0.065 - inflacion/100
        }

        # --- Función de cálculo modificada ---
        def calcular_crecimiento_detallado(clase, tasa):
            meses_total = años * 12
            tasa_mensual = (1 + tasa) ** (1/12) - 1
            crecimiento_mensual = (1 + crecimiento_aportes/100) ** (1/12)
            
            saldo = capital_inicial * (st.session_state.asignacion[clase]/100)
            aportes_acumulados = capital_inicial * (st.session_state.asignacion[clase]/100)
            crecimiento_acumulado = 0.0
            historial = {'Aportes': [], 'Crecimiento': [], 'Total': []}
            
            aporte_actual = aporte_mensual * (st.session_state.asignacion[clase]/100)
            
            for mes in range(1, meses_total + 1):
                # Calcular crecimiento del período
                crecimiento = saldo * tasa_mensual
                saldo += crecimiento + aporte_actual
                
                # Acumular valores
                aportes_acumulados += aporte_actual
                crecimiento_acumulado += crecimiento
                
                # Registrar anualmente
                if mes % 12 == 0:
                    historial['Aportes'].append(aportes_acumulados)
                    historial['Crecimiento'].append(crecimiento_acumulado)
                    historial['Total'].append(saldo)
                
                aporte_actual *= crecimiento_mensual
            
            return historial

        # Generar datos para el gráfico
        datos_clases = {
            clase: calcular_crecimiento_detallado(clase, tasa)
            for clase, tasa in tasas.items()
        }

        # Crear DataFrame consolidado
        df = pd.DataFrame({
            'Año': np.tile(np.arange(1, años + 1), 3),
            'Clase': np.repeat(['Renta Fija', 'Renta Variable', 'Alternativos'], años),
            'Aportes': np.concatenate([datos_clases['Renta Fija']['Aportes'],
                                    datos_clases['Renta Variable']['Aportes'],
                                    datos_clases['Alternativos']['Aportes']]),
            'Crecimiento': np.concatenate([datos_clases['Renta Fija']['Crecimiento'],
                                        datos_clases['Renta Variable']['Crecimiento'],
                                        datos_clases['Alternativos']['Crecimiento']])
        })

        # --- Crear gráfico de componentes ---
        fig = px.bar(df, 
                    x='Año', 
                    y=['Aportes', 'Crecimiento'], 
                    color='Clase',
                    title="Desglose del Crecimiento: Capital Humano vs. Financiero",
                    labels={'value': 'Valor (USD)', 'variable': 'Componente'},
                    barmode='relative',
                    facet_col='Clase',
                    category_orders={'Clase': ['Renta Fija', 'Renta Variable', 'Alternativos']})

        # Añadir línea de tendencia exponencial
        for i, clase in enumerate(['Renta Fija', 'Renta Variable', 'Alternativos'], 1):
            sub_df = df[df['Clase'] == clase]
            total = sub_df['Aportes'] + sub_df['Crecimiento']
            fig.add_scatter(x=sub_df['Año'], y=total, 
                            mode='lines+markers', 
                            name=f'Tendencia {clase}',
                            line=dict(width=3, dash='dot'),
                            row=1, col=i)

        fig.update_layout(
            height=600,
            legend=dict(orientation='h', yanchor='bottom', y=1.02),
            hovermode="x unified",
            annotations=[
                dict(
                    text="💡 El área azul muestra tus aportes (Capital Humano)<br>El área naranja muestra el crecimiento generado (Capital Financiero)<br>Línea punteada: Efecto del interés compuesto",
                    x=0.5,
                    y=-0.25,
                    showarrow=False,
                    xref="paper",
                    yref="paper",
                    align="left"
                )
            ]
        )

        # Mostrar gráfico
        st.plotly_chart(fig, use_container_width=True)

        # Mostrar métricas
        total_proyectado = sum([sum(datos_clases[clase]['Total']) for clase in tasas.keys()])
        col_m1, col_m2 = st.columns(2)
        with col_m1:
            st.metric("Valor final proyectado", f"${total_proyectado:,.2f}")
            st.metric("Total aportado", f"${capital_inicial + aporte_mensual * 12 * años:,.2f}")
        with col_m2:
            st.metric("Crecimiento real estimado", f"{((total_proyectado/(capital_inicial + aporte_mensual * 12 * años)) - 1):.1%}")
            st.metric("Pérdida por inflación", f"${(capital_inicial + aporte_mensual * 12 * años) * (1 + inflacion/100)**años - (capital_inicial + aporte_mensual * 12 * años):,.2f}")

# --- DISCLAIMER LEGAL ---
st.markdown("---")
st.markdown("""
**📜 Descargo de Responsabilidad Completo:**  
*Este simulador financiero tiene únicamente fines educativos e ilustrativos. Los resultados mostrados son proyecciones hipotéticas basadas en supuestos históricos y no garantizan resultados futuros.  
Las tasas de rendimiento utilizadas son promedios históricos ajustados y no reflejan el desempeño de inversiones específicas.  
La inversión en mercados financieros conlleva riesgos, incluida la posible pérdida del capital invertido.  
Se recomienda consultar con un asesor financiero certificado antes de tomar cualquier decisión de inversión.  
El autor y desarrollador no asumen responsabilidad alguna por decisiones tomadas basadas en la información aquí proporcionada.*  
*Versión 2.2 - Mayo 2025 - Todos los derechos reservados*
""")

# Estilos CSS personalizados
st.markdown("""
<style>
    .stMetric { background-color: #000000; padding: 20px; border-radius: 10px; }
    .st-bq { font-size: 1.1rem; }
    .st-cj { color: #2c3e50; }
    .st-dh { box-shadow: 0 2px 8px rgba(0,0,0,0.1); }
</style>
""", unsafe_allow_html=True)
