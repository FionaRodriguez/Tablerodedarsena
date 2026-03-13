import sqlite3
from datetime import datetime
from pathlib import Path

import pandas as pd
import streamlit as st
from streamlit_autorefresh import st_autorefresh

import streamlit.components.v1 as components

# =========================================================
# CONFIGURACION GENERAL
# =========================================================
st.set_page_config(
    page_title="Transferencias Logística",
    page_icon="🚚",
    layout="wide",
    initial_sidebar_state="expanded",
)

PASSWORD_CORRECTA = "logistica.2026"
DB_PATH = Path("logistica.db")
REFRESH_MS = 1000
MAX_FILAS_DASHBOARD = 12

st_autorefresh(interval=REFRESH_MS, key="refresh_app")

# =========================================================
# ESTILOS
# =========================================================
st.markdown(
    """
    <style>
    :root {
        --bg: #edf2f7;
        --card: #ffffff;
        --border: #d8e1ec;
        --blue: #2f5db8;
        --blue-dark: #244b96;
        --text: #152033;
        --muted: #5d6b82;
        --row-red: #f6dfe2;
        --row-yellow: #fff2c9;
        --row-green: #dff0e2;
        --row-blue: #e2ebfa;
    }

    .stApp {
    background: #0c1424;
    }

    header[data-testid="stHeader"]{
        background: #0c1424 !important;
    }

    header[data-testid="stToolbar"]{
        background: #0c1424 !important;
    }

    div[data-testid="stDecoration"]{
        background: #0c1424 !important;
    }

    div[data-testid="stAppViewContainer"]{
        background: #0c1424 !important;
    }

    main[data-testid="stMain"]{
        background: #0c1424 !important;
    }

    .block-container {
        max-width: 1480px;
        padding-top: 0.9rem;
        padding-bottom: 0.7rem;
    }

    header[data-testid="stHeader"] {
        background: var(--bg);
    }

    section[data-testid="stSidebar"] {
        background: #ffffff;
        border-right: 1px solid var(--border);
    }

    section[data-testid="stSidebar"] * {
        color: var(--text) !important;
    }

    .top-box {
        background: var(--blue);
        color: white;
        border-radius: 12px;
        min-height: 74px;
        display: flex;
        align-items: center;
        padding: 0 22px;
        box-sizing: border-box;
        margin-bottom: 12px;
        box-shadow: 0 1px 2px rgba(0,0,0,0.04);
    }

    .top-title {
        font-size: 1.95rem;
        font-weight: 800;
        letter-spacing: 0.3px;
    }

    .top-update {
        font-size: 1.15rem;
        font-weight: 700;
        justify-content: flex-start;
        text-align: left;
    }

    .section-title {
        background: var(--blue);
        color: white;
        border-radius: 12px 12px 0 0;
        padding: 12px 16px;
        font-size: 1.35rem;
        font-weight: 800;
        letter-spacing: 0.2px;
    }

    .card-body {
        background: var(--card);
        border: 1px solid var(--border);
        border-top: none;
        border-radius: 0 0 12px 12px;
        padding: 18px 18px 20px 18px;
        box-sizing: border-box;
    }

    .next-card {
        min-height: 470px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }

    .next-line {
        font-size: 1.22rem;
        line-height: 1.4;
        margin-bottom: 14px;
        color: var(--text);
    }

    .next-label {
        color: var(--blue-dark);
        font-weight: 800;
    }

    .next-empty {
        font-size: 1.15rem;
        color: var(--text);
        margin-bottom: 12px;
    }

    .bgh-wrap {
        width: 100%;
        display: flex;
        justify-content: center;
        align-items: flex-end;
        margin-top: 28px;
        padding-top: 12px;
    }

    .bgh-fallback {
        font-size: 4.6rem;
        font-weight: 900;
        color: var(--blue-dark);
        line-height: 1;
        letter-spacing: 1px;
    }

    .login-box {
        max-width: 900px;
        margin: 60px auto 0 auto;
    }

    .helper {
        color: var(--muted);
        font-size: 0.92rem;
        margin-top: 6px;
    }

    div[data-testid="stDataFrame"] {
        border-radius: 0 0 12px 12px;
        overflow: hidden;
        border: 1px solid var(--border);
        border-top: none;
    }
    
    div[data-testid="stDataFrame"] table {
    background: white !important;
    }

    div[data-testid="stDataFrame"] td {
        background: white !important;
        color: black !important;
    }

    div[data-testid="stDataFrame"] th {
        background: #f2f4f8 !important;
        color: black !important;
    }
    
    div[data-testid="stDataFrame"] [role="grid"] {
    background: white !important;
    }

    div[data-testid="stDataFrame"] [data-testid="stDataFrameResizable"] {
        background: white !important;
    }

    div[data-testid="stDataFrame"] canvas {
        background: white !important;
    }

    div[data-testid="stDataFrameGlideDataEditor"] {
        background: white !important;
    }

    div[data-testid="stDataFrame"] * {
        color: black !important;
    }
    
    .tabla-wrap{
        width: 100%;
        max-height: 520px;
        overflow-y: auto;
        overflow-x: auto;
        background: #ffffff;
        border: 1px solid #000000;
        border-top: none;
        box-sizing: border-box;
    }

    .tabla-transferencias{
        width: 100%;
        border-collapse: collapse !important;
        table-layout: auto;
        background: #ffffff !important;
        color: #000000 !important;
        margin: 0;
    }

    .tabla-transferencias thead th{
        background: #ffffff !important;
        color: #000000 !important;
        border: 1px solid #000000 !important;
        padding: 10px 12px !important;
        text-align: left !important;
        font-weight: 700 !important;
    }

    .tabla-transferencias tbody td{
        background: #ffffff;
        color: #000000;
        border: 1px solid #000000;
        padding: 10px 12px;
        text-align: left;
    }
   
    .fila-finalizado td{
    background: #dbe8ff !important;
    color: #000000 !important;
    }

    .fila-retrasado td{
        background: #f8d7da !important;
        color: #000000 !important;
    }

    .fila-arribando td{
        background: #fff3cd !important;
        color: #000000 !important;
    }

    .fila-proximo td{
        background: #d4edda !important;
        color: #000000 !important;
    }

    .fila-pendiente td{
        background: #ffffff !important;
        color: #000000 !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# =========================================================
# BASE DE DATOS
# =========================================================
def get_connection():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS transferencias (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fecha TEXT NOT NULL,
            hora TEXT NOT NULL,
            fechahora TEXT NOT NULL,
            zimp TEXT,
            transporte TEXT NOT NULL,
            checklist INTEGER NOT NULL DEFAULT 0,
            creado_en TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
        )
        """
    )
    conn.commit()
    return conn


def cargar_datos():
    conn = get_connection()
    df = pd.read_sql_query(
        "SELECT * FROM transferencias ORDER BY datetime(fechahora) ASC",
        conn,
    )
    conn.close()

    if df.empty:
        return df

    df["fechahora_dt"] = pd.to_datetime(df["fechahora"], errors="coerce")
    df["checklist"] = df["checklist"].astype(bool)
    return df


def insertar_fila(fecha: str, hora: str, zimp: str, transporte: str, checklist: bool):
    fecha_dt = datetime.strptime(fecha, "%d/%m/%Y")
    hora_dt = datetime.strptime(hora, "%H:%M").time()
    fechahora = datetime.combine(fecha_dt.date(), hora_dt)

    conn = get_connection()
    conn.execute(
        """
        INSERT INTO transferencias (fecha, hora, fechahora, zimp, transporte, checklist)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            fecha,
            hora,
            fechahora.strftime("%Y-%m-%d %H:%M:%S"),
            zimp.strip() if zimp else "",
            transporte.strip().upper(),
            int(checklist),
        ),
    )
    conn.commit()
    conn.close()


def actualizar_checklist(id_fila: int, valor: bool):
    conn = get_connection()
    conn.execute(
        "UPDATE transferencias SET checklist = ? WHERE id = ?",
        (int(valor), id_fila),
    )
    conn.commit()
    conn.close()


def eliminar_fila(id_fila: int):
    conn = get_connection()
    conn.execute("DELETE FROM transferencias WHERE id = ?", (id_fila,))
    conn.commit()
    conn.close()

# =========================================================
# LOGIN
# =========================================================
def acceso_carga_edicion():
    if "autenticado_carga" not in st.session_state:
        st.session_state.autenticado_carga = False

    if st.session_state.autenticado_carga:
        return True

    st.markdown('<div class="top-box"><div class="top-title">ACCESO A CARGA Y EDICIÓN</div></div>', unsafe_allow_html=True)

    with st.form("login_carga_form"):
        password = st.text_input("Contraseña", type="password")
        submitted = st.form_submit_button("Ingresar")

        if submitted:
            if password == PASSWORD_CORRECTA:
                st.session_state.autenticado_carga = True
                st.rerun()
            else:
                st.error("Contraseña incorrecta")

    return False

# =========================================================
# LOGICA DE NEGOCIO
# =========================================================
def calcular_estado(fechahora: datetime, checklist: bool, ahora: datetime):
    if checklist:
        return "FINALIZADO"

    delta_min = (fechahora - ahora).total_seconds() / 60

    if delta_min < 0:
        return "RETRASADO"
    if 0 <= delta_min <= 5:
        return "ARRIBANDO"
    if 5 < delta_min <= 30:
        return "PROXIMO ARRIBO"
    return "PENDIENTE"

def clase_fila_estado(estado):
    if estado == "FINALIZADO":
        return "fila-finalizado"
    if estado == "RETRASADO":
        return "fila-retrasado"
    if estado == "ARRIBANDO":
        return "fila-arribando"
    if estado == "PROXIMO ARRIBO":
        return "fila-proximo"
    return "fila-pendiente"

def es_estado_proxima_transferencia(estado):
    return estado in ["ARRIBANDO", "PROXIMO ARRIBO", "PENDIENTE"]

def armar_tabla_dashboard(df: pd.DataFrame):
    ahora = datetime.now()
    tabla = df.copy()
    if tabla.empty:
        return tabla

    tabla["ESTADO"] = tabla.apply(
        lambda row: calcular_estado(row["fechahora_dt"], row["checklist"], ahora),
        axis=1,
    )
    tabla["HORA"] = tabla["fechahora_dt"].dt.strftime("%H:%M")
    tabla["FECHAHORA_TEXTO"] = tabla["fechahora_dt"].dt.strftime("%d/%m/%Y %H:%M")
    return tabla


def obtener_proximo_arribo(tabla: pd.DataFrame):
    if tabla.empty:
        return None
    candidatos = tabla[tabla["ESTADO"].isin(["ARRIBANDO", "PROXIMO ARRIBO", "PENDIENTE"])].copy()
    if candidatos.empty:
        return None
    candidatos = candidatos.sort_values("fechahora_dt", ascending=True)
    return candidatos.iloc[0]


def formato_regresivo(objetivo: datetime):
    delta = objetivo - datetime.now()
    segundos = max(int(delta.total_seconds()), 0)
    horas = segundos // 3600
    minutos = (segundos % 3600) // 60
    segundos_restantes = segundos % 60

    if horas > 0:
        return f"{horas} h {minutos} min"
    if minutos > 0:
        return f"{minutos} min {segundos_restantes} s"
    return f"{segundos_restantes} s"

# =========================================================
# VISTAS
# =========================================================
def vista_carga():
    st.markdown('<div class="top-box"><div class="top-title">CARGA Y EDICIÓN DE TRANSFERENCIAS</div></div>', unsafe_allow_html=True)

    df = cargar_datos()

    registro_editar = None
    if "editar_id" in st.session_state and not df.empty:
        fila_edit = df[df["id"] == st.session_state["editar_id"]]
        if not fila_edit.empty:
            registro_editar = fila_edit.iloc[0]
    
    with st.expander("Agregar nueva fila", expanded=True):
        with st.form("form_agregar"):

            # valores por defecto
            fecha_default = datetime.now().date()
            hora_default = datetime.now().replace(second=0, microsecond=0).time()
            zimp_default = ""
            transporte_default = "VESPRINI"
            checklist_default = False

            if registro_editar is not None:
                fecha_default = datetime.strptime(registro_editar["fecha"], "%d/%m/%Y").date()
                hora_default = datetime.strptime(registro_editar["hora"], "%H:%M").time()
                zimp_default = registro_editar["zimp"] if registro_editar["zimp"] else ""
                transporte_default = registro_editar["transporte"]
                checklist_default = bool(registro_editar["checklist"])

            c1, c2, c3, c4, c5 = st.columns(5)
            with c1:
                fecha_input = st.date_input("Fecha", value=fecha_default)

            with c2:
                hora_input = st.time_input("Hora", value=hora_default, step=1800)

            with c3:
                zimp_input = st.text_input("ZIMP", value=zimp_default)

            with c4:
                transporte_input = st.text_input("Transporte", value=transporte_default)

            with c5:
                checklist_input = st.checkbox("Checklist realizado", value=checklist_default)

            guardar = st.form_submit_button("Guardar fila")
            if guardar:
                if not transporte_input.strip():
                    st.error("El transporte no puede quedar vacío.")
                else:
                    insertar_fila(
                        fecha_input.strftime("%d/%m/%Y"),
                        hora_input.strftime("%H:%M"),
                        zimp_input,
                        transporte_input,
                        checklist_input,
                    )
                    st.success("Fila agregada correctamente")
                    st.rerun()

    df = cargar_datos()
    if df.empty:
        st.info("Todavía no hay registros cargados.")
        return

    st.markdown("### Registros actuales")
    for _, row in df.iterrows():
        c1, c2, c3, c4, c5, c6, c7 = st.columns([1.0, 1.2, 2.0, 1.5, 1.8, 1.1, 0.8])
        with c1:
            st.write(row["hora"])
        with c2:
            st.write(row["fecha"])
        with c3:
            st.write(row["fechahora_dt"].strftime("%d/%m/%Y %H:%M"))
        with c4:
            st.write(row["zimp"] if row["zimp"] else "-")
        with c5:
            st.write(row["transporte"])
        with c6:
            nuevo_check = st.checkbox(
                "Hecho",
                value=bool(row["checklist"]),
                key=f"chk_carga_{row['id']}",
                label_visibility="collapsed",
            )
            if nuevo_check != bool(row["checklist"]):
                actualizar_checklist(int(row["id"]), nuevo_check)
                st.rerun()
        with c7:
            col_edit, col_del = st.columns(2)

            with col_edit:
                if st.button("✏️", key=f"edit_{row['id']}"):
                    st.session_state["editar_id"] = int(row["id"])
                    st.rerun()

            with col_del:
                if st.button("🗑", key=f"del_{row['id']}"):
                    eliminar_fila(int(row["id"]))
                    st.rerun()

def vista_comprobacion():
    st.markdown('<div class="top-box"><div class="top-title">COMPROBACIÓN</div></div>', unsafe_allow_html=True)

    df = cargar_datos()
    if df.empty:
        st.info("Todavía no hay registros cargados.")
        return

    st.markdown("### Registros actuales")

    # encabezado
    h1, h2, h3, h4, h5, h6 = st.columns([1.0, 1.2, 2.0, 1.5, 1.8, 1.1])
    with h1:
        st.markdown("**Hora**")
    with h2:
        st.markdown("**Fecha**")
    with h3:
        st.markdown("**Fecha y hora**")
    with h4:
        st.markdown("**ZIMP**")
    with h5:
        st.markdown("**Transporte**")
    with h6:
        st.markdown("**Checklist**")

    st.markdown("---")

    for _, row in df.iterrows():
        with st.container(border=True):
            c1, c2, c3, c4, c5, c6 = st.columns([1.0, 1.2, 2.0, 1.5, 1.8, 1.1])

            with c1:
                st.markdown(f"<span style='color:white;; font-weight:600'>{row['hora']}</span>", unsafe_allow_html=True)
            with c2:
                st.markdown(f"<span style='color:white; font-weight:600'>{row['fecha']}</span>", unsafe_allow_html=True)
            with c3:
                st.markdown(
                    f"<span style='color:white; font-weight:600'>{row['fechahora_dt'].strftime('%d/%m/%Y %H:%M')}</span>",
                    unsafe_allow_html=True
                )
            with c4:
                st.markdown(
                    f"<span style='color:white; font-weight:600'>{row['zimp'] if row['zimp'] else '-'}</span>",
                    unsafe_allow_html=True
                )
            with c5:
                st.markdown(f"<span style='color:white; font-weight:600'>{row['transporte']}</span>", unsafe_allow_html=True)
            with c6:
                nuevo_check = st.checkbox(
                    "Hecho",
                    value=bool(row["checklist"]),
                    key=f"chk_comprobacion_{row['id']}",
                    label_visibility="collapsed",
                )
                if nuevo_check != bool(row["checklist"]):
                    actualizar_checklist(int(row["id"]), nuevo_check)
                    st.rerun()

def vista_dashboard():
    df = cargar_datos()
    tabla = armar_tabla_dashboard(df) if not df.empty else pd.DataFrame()

    c1, c2 = st.columns([1.75, 1.0], gap="small")
    with c1:
        st.markdown('<div class="top-box"><div class="top-title">TRANSFERENCIAS</div></div>', unsafe_allow_html=True)
    with c2:
       ultima = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
       st.markdown(f'<div class="top-box top-title">{ultima}</div>', unsafe_allow_html=True)

    c1, c2 = st.columns([1.75, 1.0], gap="small")

    with c1:
        st.markdown('<div class="section-title">TABLERO DE DÁRSENA</div>', unsafe_allow_html=True)
        if tabla.empty:
            st.markdown('<div class="card-body">No hay datos cargados todavía.</div>', unsafe_allow_html=True)
        else:
            vista = tabla[["fechahora_dt", "HORA", "zimp", "ESTADO", "transporte", "checklist"]].copy()

            # numeración del día
            vista["N°"] = vista.groupby(vista["fechahora_dt"].dt.date).cumcount() + 1

            vista = vista[["N°", "HORA", "zimp", "ESTADO", "transporte", "checklist"]]

            vista.columns = ["N°", "HORA", "ZIMP", "ESTADO", "TRANSPORTE", "CHECKLIST"]
            vista["ZIMP"] = vista["ZIMP"].replace("", "-")
            # mostrar todas las transferencias para que exista scroll
            vista = vista.copy()

            vista["CHECKLIST_TEXTO"] = vista["CHECKLIST"].apply(lambda x: "✓" if x else "")
            proximo_id = None

            tabla_html = """<div class="tabla-wrap">
            <table class="tabla-transferencias">
            <thead>
            <tr>
            <th>N°</th>
            <th>HORA</th>
            <th>ZIMP</th>
            <th>ESTADO</th>
            <th>TRANSPORTE</th>
            <th>CHECKLIST</th>
            </tr>
            </thead>
            <tbody>
            """

            for _, row in vista.iterrows():
                clase_fila = clase_fila_estado(row["ESTADO"])

                fila_id_html = ""
                if proximo_id is None and es_estado_proxima_transferencia(row["ESTADO"]):
                    proximo_id = row["N°"]
                    fila_id_html = f'id="fila-proxima-{row["N°"]}"'

                tabla_html += f"""<tr class="{clase_fila}" {fila_id_html}>
            <td>{row['N°']}</td>
            <td>{row['HORA']}</td>
            <td>{row['ZIMP']}</td>
            <td>{row['ESTADO']}</td>
            <td>{row['TRANSPORTE']}</td>
            <td>{row['CHECKLIST_TEXTO']}</td>
            </tr>
            """

            tabla_html += "</tbody></table></div>"

            css_tabla = """
            <style>
                body {
                    margin: 0;
                    padding: 0;
                    background: transparent;
                    font-family: Arial, sans-serif;
                }

                .tabla-wrap{
                    width: 100%;
                    max-height: 470px;
                    overflow-y: auto;
                    overflow-x: auto;
                    background: #ffffff;
                    border: 1px solid #000000;
                    border-top: none;
                    box-sizing: border-box;
                }

                .tabla-transferencias{
                    width: 100%;
                    border-collapse: collapse;
                    table-layout: auto;
                    background: #ffffff;
                    color: #000000;
                    margin: 0;
                }

                .tabla-transferencias thead th{
                    background: #ffffff;
                    color: #000000;
                    border: 1px solid #000000;
                    padding: 10px 12px;
                    text-align: left;
                    font-weight: 700;
                    position: sticky;
                    top: 0;
                    z-index: 2;
                }

                .tabla-transferencias tbody td{
                    background: #ffffff;
                    color: #000000;
                    border: 1px solid #000000;
                    padding: 10px 12px;
                    text-align: left;
                }

                .fila-finalizado td{
                    background: #dbe8ff !important;
                    color: #000000 !important;
                }

                .fila-retrasado td{
                    background: #f8d7da !important;
                    color: #000000 !important;
                }

                .fila-arribando td{
                    background: #fff3cd !important;
                    color: #000000 !important;
                }

                .fila-proximo td{
                    background: #fff3cd !important;
                    color: #000000 !important;
                }

                .fila-pendiente td{
                    background: #ffffff !important;
                    color: #000000 !important;
                }
                [data-testid="stVerticalBlock"] div[data-testid="stContainer"] {
                    background: #ffffff;
                    border-radius: 12px;
                }

                [data-testid="stVerticalBlock"] div[data-testid="stContainer"] p {
                    color: #000000 !important;
                }
            </style>
            """

            script_scroll = ""
            if proximo_id is not None:
                script_scroll = f"""
                <script>
                window.addEventListener("load", function() {{
                    const contenedor = document.querySelector(".tabla-wrap");
                    const fila = document.getElementById("fila-proxima-{proximo_id}");

                    if (contenedor && fila) {{
                        const topFila = fila.offsetTop;
                        const altoFila = fila.offsetHeight;
                        const altoContenedor = contenedor.clientHeight;

                        contenedor.scrollTop = topFila - (altoContenedor / 2) + (altoFila / 2);
                    }}
                }});
                </script>
                """

            html_completo = css_tabla + tabla_html + script_scroll

            components.html(html_completo, height=540, scrolling=False)

    with c2:
        st.markdown('<div class="section-title">PRÓXIMA TRANSFERENCIA</div>', unsafe_allow_html=True)
        proximo = obtener_proximo_arribo(tabla) if not tabla.empty else None

        if proximo is None:
            st.markdown(
                '''
                <div class="card-body next-card">
                    <div class="next-empty">No hay transferencias próximas pendientes.</div>
                    <div class="bgh-wrap"><div class="bgh-fallback">BGH</div></div>
                </div>
                ''',
                unsafe_allow_html=True,
            )
        else:
            fecha_hora = proximo["fechahora_dt"].strftime("%d/%m/%Y %H:%M")
            zimp = proximo["zimp"] if proximo["zimp"] else "-"
            transporte = proximo["transporte"]
            falta = formato_regresivo(proximo["fechahora_dt"])

            st.markdown(
                f'''
                <div class="card-body next-card">
                    <div>
                        <div class="next-line"><span class="next-label">Fecha y hora:</span> {fecha_hora}</div>
                        <div class="next-line"><span class="next-label">ZIMP:</span> {zimp}</div>
                        <div class="next-line"><span class="next-label">Transporte:</span> {transporte}</div>
                        <div class="next-line"><span class="next-label">Falta:</span> {falta}</div>
                        <div class="next-line"><span class="next-label">Estado:</span> {proximo['ESTADO']}</div>
                    </div>
                    <div class="bgh-wrap"><div class="bgh-fallback">BGH</div></div>
                </div>
                ''',
                unsafe_allow_html=True,
            )

# =========================================================
# APP
# =========================================================
def main():

    st.sidebar.title("Menú")
    vista = st.sidebar.radio("Ir a", ["Dashboard", "Comprobación", "Carga y edición"])
    st.sidebar.markdown("---")

    if vista == "Dashboard":
        vista_dashboard()
    elif vista == "Comprobación":
        vista_comprobacion()
    else:
        if acceso_carga_edicion():
            vista_carga()


if __name__ == "__main__":
    main()
