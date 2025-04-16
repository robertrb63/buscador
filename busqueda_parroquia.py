import streamlit as st
import json
import pandas as pd

# Configuración de la página
st.set_page_config(page_title="Búsqueda y Gestión de Parroquias", layout="wide")
st.markdown(
    """
    <style>
    .main {
        background-color: #e6f3fa;
        padding: 20px;
    }
    h1 {
        color: #2c3e50;
        font-family: Helvetica, sans-serif;
        font-size: 24px;
        font-weight: bold;
        text-align: center;
    }
    .stButton>button {
        background-color: #4a90e2;
        color: white;
        font-family: Helvetica, sans-serif;
        font-size: 16px;
        padding: 10px 20px;
        border-radius: 5px;
    }
    .stTextInput>div>input {
        font-family: Helvetica, sans-serif;
        font-size: 16px;
    }
    .stDataFrame {
        width: 100%;
        overflow-x: auto;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Título
st.title("Sistema de Búsqueda y Gestión de Parroquias")

# Nombre del archivo JSON
ARCHIVO_JSON = "data.json"

# Funciones para manejar datos
def cargar_datos():
    """Carga todos los datos del archivo JSON, eliminando duplicados."""
    try:
        with open(ARCHIVO_JSON, 'r', encoding='utf-8') as file:
            datos = json.load(file)
        datos_unicos = []
        seen = set()
        for persona in datos:
            persona_tuple = tuple(persona.items())
            if persona_tuple not in seen:
                seen.add(persona_tuple)
                datos_unicos.append(persona)
        return datos_unicos
    except FileNotFoundError:
        st.error(f"No se encontró el archivo {ARCHIVO_JSON}")
        return []
    except json.JSONDecodeError:
        st.error("El archivo JSON no es válido")
        return []
    except Exception as e:
        st.error(f"Ocurrió un error: {str(e)}")
        return []

def buscar_parroquia(parroquia_buscada, datos):
    """Filtra los datos por parroquia (insensible a mayúsculas/minúsculas)."""
    if not parroquia_buscada or parroquia_buscada == "Ej: Graus":
        return datos
    return [persona for persona in datos if parroquia_buscada.lower() in persona['parroquia'].lower()]

def guardar_registro(nuevo_registro):
    """Guarda un nuevo registro en el archivo JSON."""
    try:
        try:
            with open(ARCHIVO_JSON, 'r', encoding='utf-8') as file:
                datos = json.load(file)
        except FileNotFoundError:
            datos = []
        except json.JSONDecodeError:
            st.error("El archivo JSON no es válido")
            return False

        if any(persona['id'] == nuevo_registro['id'] for persona in datos):
            st.error("El ID ya existe. Use un ID único.")
            return False

        datos.append(nuevo_registro)
        try:
            with open(ARCHIVO_JSON, 'w', encoding='utf-8') as file:
                json.dump(datos, file, indent=4, ensure_ascii=False)
            return True
        except PermissionError:
            st.error("No se tiene permiso para escribir en el archivo data.json.")
            return False
        except Exception as e:
            st.error(f"Error al escribir en el archivo: {str(e)}")
            return False
    except Exception as e:
        st.error(f"Ocurrió un error al guardar: {str(e)}")
        return False

# Estado para manejar la búsqueda
if 'search_term' not in st.session_state:
    st.session_state.search_term = "Ej: Graus"

# Layout con columnas para búsqueda y botones
col1, col2, col3 = st.columns([4, 1, 1])
with col1:
    search_input = st.text_input("Ingrese el nombre de la parroquia:", value=st.session_state.search_term, key="search_input")
with col2:
    if st.button("Buscar"):
        if search_input == "Ej: Graus" or not search_input.strip():
            st.warning("Por favor, ingrese el nombre de una parroquia.")
        else:
            st.session_state.search_term = search_input
with col3:
    if st.button("Limpiar"):
        st.session_state.search_term = "Ej: Graus"
        st.rerun()

# Cargar datos
datos = cargar_datos()

# Filtrar datos según búsqueda
resultados = buscar_parroquia(st.session_state.search_term, datos)
if not resultados and st.session_state.search_term != "Ej: Graus" and st.session_state.search_term.strip():
    st.info(f"No se encontraron registros para la parroquia: {st.session_state.search_term}")

# Mostrar tabla
if resultados:
    df = pd.DataFrame(resultados, columns=[
        "id", "nombre", "telefono", "email", "parroquia", "grupoParroquial", "UnidadPastoral",
        "moderador", "telModerador", "arciprestazgo", "telArciprestazgo", "arcipreste","animador", "telAnimador"
    ])
    st.dataframe(
        df,
        use_container_width=True,
        height=300,
        column_config={
            "id": st.column_config.NumberColumn("ID", width="small"),
            "nombre": st.column_config.TextColumn("Nombre", width="medium"),
            "telefono": st.column_config.TextColumn("Teléfono", width="medium"),
            "email": st.column_config.TextColumn("Email", width="large"),
            "parroquia": st.column_config.TextColumn("Parroquia", width="medium"),
            "grupoParroquial": st.column_config.TextColumn("Grupo Parroquial", width="medium"),
            "UnidadPastoral": st.column_config.TextColumn("Unidad Pastoral", width="medium"),
            "moderador": st.column_config.TextColumn("Moderador", width="medium"),
            "telModerador": st.column_config.TextColumn("Tel. Moderador", width="medium"),
            "arciprestazgo": st.column_config.TextColumn("Arciprestazgo", width="medium"),
            "arcipreste": st.column_config.TextColumn("Arcipreste", width="medium"),
            "telArciprestazgo": st.column_config.TextColumn("Tel. Arciprestazgo", width="medium"),
            "animador": st.column_config.TextColumn("Animador", width="medium"),
            "telAnimador": st.column_config.TextColumn("Tel. Animador", width="medium"),
        }
    )
elif st.session_state.search_term == "Ej: Graus" or not st.session_state.search_term.strip():
    st.write("Ingrese una parroquia para buscar o agregue un nuevo registro.")
else:
    st.write("No hay datos para mostrar.")

# Formulario para agregar nuevo registro
st.subheader("Agregar Nuevo Registro")
with st.form(key="agregar_form"):
    campos = [
        ("ID", "id", "number"),
        ("Nombre", "nombre", "text"),
        ("Teléfono", "telefono", "text"),
        ("Email", "email", "text"),
        ("Parroquia", "parroquia", "text"),
        ("Grupo Parroquial", "grupoParroquial", "text"),
        ("Unidad Pastoral", "UnidadPastoral", "text"),
        ("Moderador", "moderador", "text"),
        ("Tel. Moderador", "telModerador", "text"),
        ("Arciprestazgo", "arciprestazgo", "text"),
        ("Arcipreste", "arcipreste", "text"),
        ("Tel. Arciprestazgo", "telArciprestazgo", "text"),
        ("Animador", "animador", "text"),
        ("Tel. Animador", "telAnimador", "text")
    ]

    default_id = 1
    if datos:
        default_id = max(persona['id'] for persona in datos) + 1

    col_left, col_right = st.columns(2)
    valores = {}
    for i, (label, key, input_type) in enumerate(campos):
        col = col_left if i % 2 == 0 else col_right
        with col:
            if input_type == "number":
                valores[key] = st.number_input(label, min_value=1, value=default_id if key == "id" else 0, step=1)
            else:
                valores[key] = st.text_input(label, value="")

    submit_button = st.form_submit_button("Guardar")

    if submit_button:
        nuevo_registro = {}
        for key, valor in valores.items():
            if key == "id":
                if not isinstance(valor, int) or valor <= 0:
                    st.error("El ID debe ser un número entero positivo.")
                    st.stop()
                nuevo_registro[key] = int(valor)
            else:
                if not valor.strip():
                    st.error(f"El campo {key} no puede estar vacío.")
                    st.stop()
                nuevo_registro[key] = valor.strip()

        if guardar_registro(nuevo_registro):
            st.success("Registro agregado y guardado correctamente en data.json.")
            st.session_state.search_term = "Ej: Graus"
            st.rerun()
