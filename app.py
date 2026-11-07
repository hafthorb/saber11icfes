import joblib
import numpy as np
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Nivel Saber 11", page_icon="🎓", layout="wide")

@st.cache_resource
def cargar_modelo():
    modelo = joblib.load("modelofinal_saber11.pkl")
    codificador = joblib.load("label_encoder.pkl")
    return modelo, codificador

modelo, le = cargar_modelo()

SI_NO = ["Si", "No"]

EDUCACION = [
    "Ninguno",
    "Primaria incompleta",
    "Primaria completa",
    "Secundaria (Bachillerato) incompleta",
    "Secundaria (Bachillerato) completa",
    "Técnica o tecnológica incompleta",
    "Técnica o tecnológica completa",
    "Educación profesional incompleta",
    "Educación profesional completa",
    "Postgrado",
    "No sabe",
    "No Aplica",
]

TRABAJO = [
    "Trabaja como profesional (por ejemplo médico, abogado, ingeniero)",
    "Es dueño de un negocio grande, tiene un cargo de nivel directivo o gerencial",
    "Es dueño de un negocio pequeño (tiene pocos empleados o no tiene, por ejemplo tienda, papelería, etc",
    "Tiene un trabajo de tipo auxiliar administrativo (por ejemplo, secretario o asistente)",
    "Trabaja por cuenta propia (por ejemplo plomero, electricista)",
    "Es vendedor o trabaja en atención al público",
    "Es operario de máquinas o conduce vehículos (taxita, chofer)",
    "Trabaja como personal de limpieza, mantenimiento, seguridad o construcción",
    "Es agricultor, pesquero o jornalero",
    "Trabaja en el hogar, no trabaja o estudia",
    "Pensionado",
    "No sabe",
]

FRECUENCIA = [
    "Nunca o rara vez comemos eso",
    "1 o 2 veces por semana",
    "3 a 5 veces por semana",
    "Todos o casi todos los días",
]

DEPARTAMENTOS = [
    "AMAZONAS", "ANTIOQUIA", "ARAUCA", "ATLANTICO", "BOGOTÁ", "BOLIVAR", "BOYACA",
    "CALDAS", "CAQUETA", "CASANARE", "CAUCA", "CESAR", "CHOCO", "CORDOBA",
    "CUNDINAMARCA", "GUAINIA", "GUAVIARE", "HUILA", "LA GUAJIRA", "MAGDALENA",
    "META", "NARIÑO", "NORTE SANTANDER", "PUTUMAYO", "QUINDIO", "RISARALDA",
    "SAN ANDRES", "SANTANDER", "SUCRE", "TOLIMA", "VALLE", "VAUPES", "VICHADA",
]

def opcion(etiqueta, opciones, por_defecto, ayuda=None):
    return st.selectbox(etiqueta, opciones, index=opciones.index(por_defecto), help=ayuda)

st.title("🎓 ¿En qué nivel quedaría en Saber 11?")
st.write(
    "Esta aplicación estima el **nivel del puntaje global** de un estudiante en la prueba Saber 11 "
    "(**Bajo**: 0 a 199, **Medio**: 200 a 296, **Alto**: 297 a 500) usando solo información sobre "
    "el estudiante, su familia y su colegio. Llena el formulario y presiona **Predecir**."
)
st.caption(
    "Modelo XGBoost entrenado con los resultados de Saber 11 del periodo 2020-2 (ICFES). "
    "Es una estimación con fines académicos: muestra asociaciones, no causas, y no reemplaza el resultado real."
)

with st.form("formulario"):
    col1, col2, col3 = st.columns(3)

    with col1:
        st.subheader("👤 Estudiante")
        genero = opcion("Género", ["F", "M"], "F")
        edad = st.number_input("Edad (años)", min_value=13, max_value=60, value=17, step=1)
        etnia = opcion("¿Pertenece a algún grupo étnico?", SI_NO, "No")
        lectura = opcion(
            "Tiempo diario de lectura por gusto",
            ["No leo por entretenimiento", "30 minutos o menos", "Entre 30 y 60 minutos",
             "Entre 1 y 2 horas", "Más de 2 horas"],
            "30 minutos o menos",
        )
        internet_uso = opcion(
            "Tiempo diario navegando en internet",
            ["No Navega Internet", "30 minutos o menos", "Entre 30 y 60 minutos",
             "Entre 1 y 3 horas", "Más de 3 horas"],
            "Entre 1 y 3 horas",
        )
        horas_trabajo = opcion(
            "Horas de trabajo a la semana",
            ["0", "Menos de 10 horas", "Entre 11 y 20 horas", "Entre 21 y 30 horas", "Más de 30 horas"],
            "0",
        )
        remuneracion = opcion(
            "¿Recibe pago por su trabajo?",
            ["No", "Si, en efectivo", "Si, en especie", "Si, en efectivo y especie"],
            "No",
        )

    with col2:
        st.subheader("🏠 Familia y hogar")
        estrato = opcion(
            "Estrato de la vivienda",
            ["Sin Estrato", "Estrato 1", "Estrato 2", "Estrato 3", "Estrato 4", "Estrato 5", "Estrato 6"],
            "Estrato 2",
        )
        personas = opcion("Personas en el hogar", ["1 a 2", "3 a 4", "5 a 6", "7 a 8", "9 o más"], "3 a 4")
        cuartos = opcion("Cuartos en el hogar", ["Uno", "Dos", "Tres", "Cuatro", "Cinco", "Seis o mas"], "Tres")
        edu_madre = opcion("Educación de la madre", EDUCACION, "Secundaria (Bachillerato) completa")
        edu_padre = opcion("Educación del padre", EDUCACION, "Secundaria (Bachillerato) completa")
        trabajo_madre = opcion("Trabajo de la madre", TRABAJO, "Trabaja en el hogar, no trabaja o estudia")
        trabajo_padre = opcion(
            "Trabajo del padre", TRABAJO,
            "Es dueño de un negocio pequeño (tiene pocos empleados o no tiene, por ejemplo tienda, papelería, etc",
        )
        situacion = opcion(
            "Situación económica frente al año anterior", ["Peor", "Igual", "Mejor"], "Igual"
        )
        libros = opcion(
            "Libros en el hogar",
            ["0 A 10 LIBROS", "11 A 25 LIBROS", "26 A 100 LIBROS", "MÁS DE 100 LIBROS"],
            "0 A 10 LIBROS",
        )

        st.markdown("**¿Qué hay en el hogar?**")
        b1, b2 = st.columns(2)
        with b1:
            tiene_internet = opcion("Internet", SI_NO, "Si")
            tiene_computador = opcion("Computador", SI_NO, "Si")
            tiene_tv = opcion("Servicio de TV", SI_NO, "Si")
            tiene_lavadora = opcion("Lavadora", SI_NO, "Si")
        with b2:
            tiene_horno = opcion("Horno microondas o a gas", SI_NO, "No")
            tiene_auto = opcion("Automóvil", SI_NO, "No")
            tiene_moto = opcion("Motocicleta", SI_NO, "No")
            tiene_consola = opcion("Consola de videojuegos", SI_NO, "No")

        st.markdown("**Alimentación de la familia**")
        come_leche = opcion("Leche y derivados", FRECUENCIA, "1 o 2 veces por semana")
        come_carne = opcion("Carne, pescado o huevo", FRECUENCIA, "Todos o casi todos los días")
        come_cereal = opcion("Cereales, frutas o legumbres", FRECUENCIA, "1 o 2 veces por semana")

    with col3:
        st.subheader("🏫 Colegio")
        naturaleza = opcion("Tipo de colegio", ["OFICIAL", "NO OFICIAL"], "OFICIAL",
                            ayuda="Oficial = público; No oficial = privado.")
        area = opcion("Zona del colegio", ["URBANO", "RURAL"], "URBANO")
        jornada = opcion("Jornada", ["MAÑANA", "TARDE", "UNICA", "COMPLETA", "NOCHE", "SABATINA"], "MAÑANA")
        caracter = opcion("Carácter del colegio",
                          ["ACADÉMICO", "TÉCNICO", "TÉCNICO/ACADÉMICO", "NO APLICA"], "ACADÉMICO")
        depto = opcion("Departamento del colegio", DEPARTAMENTOS, "BOGOTÁ")

        st.subheader("📊 Índices del ICFES")
        st.caption(
            "Estos índices los calcula el ICFES con las respuestas del cuestionario. Si no los conoces, "
            "deja el valor sugerido (el valor típico de los estudiantes)."
        )
        inse = st.slider("Índice socioeconómico del estudiante (INSE)", 0.0, 100.0, 50.6, 0.1,
                         help="Valor de 0 a 100. A mayor valor, mejores condiciones socioeconómicas.")
        nse_cole = st.select_slider("Nivel socioeconómico del colegio", options=[1, 2, 3, 4], value=2,
                                    help="De 1 (más bajo) a 4 (más alto).")

    enviado = st.form_submit_button("🔮 Predecir", use_container_width=True)

if enviado:
    datos = pd.DataFrame([{
        "ESTU_GENERO": genero,
        "ESTU_TIENEETNIA": etnia,
        "FAMI_ESTRATOVIVIENDA": estrato,
        "FAMI_PERSONASHOGAR": personas,
        "FAMI_CUARTOSHOGAR": cuartos,
        "FAMI_EDUCACIONPADRE": edu_padre,
        "FAMI_EDUCACIONMADRE": edu_madre,
        "FAMI_TRABAJOLABORPADRE": trabajo_padre,
        "FAMI_TRABAJOLABORMADRE": trabajo_madre,
        "FAMI_TIENEINTERNET": tiene_internet,
        "FAMI_TIENESERVICIOTV": tiene_tv,
        "FAMI_TIENECOMPUTADOR": tiene_computador,
        "FAMI_TIENELAVADORA": tiene_lavadora,
        "FAMI_TIENEHORNOMICROOGAS": tiene_horno,
        "FAMI_TIENEAUTOMOVIL": tiene_auto,
        "FAMI_TIENEMOTOCICLETA": tiene_moto,
        "FAMI_TIENECONSOLAVIDEOJUEGOS": tiene_consola,
        "FAMI_NUMLIBROS": libros,
        "FAMI_COMELECHEDERIVADOS": come_leche,
        "FAMI_COMECARNEPESCADOHUEVO": come_carne,
        "FAMI_COMECEREALFRUTOSLEGUMBRE": come_cereal,
        "FAMI_SITUACIONECONOMICA": situacion,
        "ESTU_DEDICACIONLECTURADIARIA": lectura,
        "ESTU_DEDICACIONINTERNET": internet_uso,
        "ESTU_HORASSEMANATRABAJA": horas_trabajo,
        "ESTU_TIPOREMUNERACION": remuneracion,
        "COLE_NATURALEZA": naturaleza,
        "COLE_CARACTER": caracter,
        "COLE_AREA_UBICACION": area,
        "COLE_JORNADA": jornada,
        "COLE_DEPTO_UBICACION": depto,
        "ESTU_INSE_INDIVIDUAL": float(inse),
        "ESTU_NSE_ESTABLECIMIENTO": float(nse_cole),
        "ESTU_EDAD": float(edad),
    }])

    columnas = modelo.named_steps["preparacion"].feature_names_in_
    datos = datos[columnas]

    prediccion = modelo.predict(datos)[0]
    probabilidades = modelo.predict_proba(datos)[0]
    nivel = le.inverse_transform([prediccion])[0]

    st.divider()
    colores = {"BAJO": "🔴", "MEDIO": "🟡", "ALTO": "🟢"}
    st.subheader(f"Resultado: {colores.get(nivel, '')} Nivel **{nivel.capitalize()}**")

    tabla = pd.DataFrame({
        "Nivel": [c.capitalize() for c in le.classes_],
        "Probabilidad": probabilidades,
    }).set_index("Nivel").loc[["Bajo", "Medio", "Alto"]]

    c1, c2 = st.columns([1, 2])
    with c1:
        st.dataframe(tabla.style.format({"Probabilidad": "{:.1%}"}), use_container_width=True)
    with c2:
        st.bar_chart(tabla)

    st.caption(
        "Las probabilidades indican qué tan seguro está el modelo. En la evaluación con datos de prueba, el modelo "
        "identificó cerca de 3 de cada 4 estudiantes de nivel Bajo y de nivel Alto, pero tiende a confundir a los "
        "estudiantes de nivel Medio con los extremos."
    )
