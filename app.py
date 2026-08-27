import streamlit as st
import os
import time
import glob
import cv2
import numpy as np
import pytesseract
from PIL import Image
from gtts import gTTS
from googletrans import Translator


# ============================================================
# CONFIGURACIÓN GENERAL
# ============================================================

st.set_page_config(
    page_title="RETRO OCR TRANSLATOR",
    page_icon="💾",
    layout="wide"
)


# ============================================================
# DISEÑO RETRO PC - AÑOS 90
# ============================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=VT323&display=swap');

html, body, [class*="css"] {
    font-family: 'VT323', monospace;
}

/* Fondo general */
.stApp {
    background-color: #101510;
    color: #b6ff8a;
}

/* Efecto CRT */
.stApp::before {
    content: "";
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    pointer-events: none;
    z-index: 9999;

    background: repeating-linear-gradient(
        0deg,
        rgba(0,0,0,0.08),
        rgba(0,0,0,0.08) 1px,
        transparent 1px,
        transparent 4px
    );
}

/* Título */
h1 {
    color: #c8ff9b !important;
    text-shadow:
        0 0 5px #78ff42,
        0 0 15px #3cff00;
    font-size: 48px !important;
    letter-spacing: 4px;
}

/* Subtítulos */
h2, h3 {
    color: #aaff66 !important;
    text-shadow: 0 0 5px #55ff00;
}

/* Texto */
p, label, div {
    color: #b6ff8a;
}

/* Paneles */
div[data-testid="stVerticalBlock"] {
    border-color: #4d703c;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #151b15;
    border-right: 3px solid #607d50;
    box-shadow: inset -4px 0px 0px #080b08;
}

/* Botones */
.stButton > button {
    background-color: #303830;
    color: #d0ffae;
    border: 3px outset #899984;
    border-radius: 0px;
    font-family: 'VT323', monospace;
    font-size: 22px;
    letter-spacing: 2px;
    box-shadow: 3px 3px 0px #050805;
}

.stButton > button:hover {
    background-color: #405040;
    color: #ffffff;
    border: 3px inset #899984;
}

/* Inputs */
.stTextInput input,
.stSelectbox,
.stRadio,
.stCheckbox {
    font-family: 'VT323', monospace;
}

/* Upload */
[data-testid="stFileUploader"] {
    background-color: #181e18;
    border: 2px dashed #718d61;
    padding: 10px;
}

/* Caja de información */
.retro-box {
    background-color: #171d17;
    border: 3px solid #687864;
    border-top-color: #a4b69b;
    border-left-color: #a4b69b;
    padding: 18px;
    margin: 10px 0px;
    box-shadow: 5px 5px 0px #050705;
}

/* Terminal */
.terminal {
    background-color: #050805;
    color: #75ff3c;
    border: 3px solid #607d50;
    padding: 15px;
    font-family: 'VT323', monospace;
    font-size: 21px;
    box-shadow:
        inset 0 0 15px rgba(50,255,50,0.15),
        5px 5px 0px #030403;
}

/* Texto pequeño */
.retro-small {
    color: #86a477;
    font-size: 17px;
}

/* Texto de sistema */
.system-text {
    color: #72ff3c;
    font-size: 19px;
}

/* Display */
.display {
    background-color: #080c08;
    border: 4px inset #6c7b67;
    padding: 12px;
    color: #69ff3d;
    font-size: 25px;
    box-shadow: inset 0 0 20px rgba(70,255,40,0.10);
}

/* Línea retro */
hr {
    border-top: 2px dashed #52694a;
}

/* Métricas */
[data-testid="stMetric"] {
    background-color: #171d17;
    border: 2px solid #687864;
    padding: 10px;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# VARIABLES
# ============================================================

text = " "


# ============================================================
# FUNCIÓN TEXTO -> AUDIO
# ============================================================

def text_to_speech(input_language, output_language, text, tld):

    translation = translator.translate(
        text,
        src=input_language,
        dest=output_language
    )

    trans_text = translation.text

    tts = gTTS(
        trans_text,
        lang=output_language,
        tld=tld,
        slow=False
    )

    try:
        my_file_name = text[0:20]
    except:
        my_file_name = "audio"

    tts.save(f"temp/{my_file_name}.mp3")

    return my_file_name, trans_text


# ============================================================
# BORRAR ARCHIVOS ANTIGUOS
# ============================================================

def remove_files(n):

    mp3_files = glob.glob("temp/*mp3")

    if len(mp3_files) != 0:

        now = time.time()
        n_days = n * 86400

        for f in mp3_files:

            if os.stat(f).st_mtime < now - n_days:

                os.remove(f)

                print("Deleted ", f)


remove_files(7)


# ============================================================
# CABECERA
# ============================================================

st.markdown("""
<div class="terminal">

<pre>
╔══════════════════════════════════════════════════════════════╗
║             ██████╗ ███████╗████████╗██████╗  ██████╗      ║
║             ██╔══██╗██╔════╝╚══██╔══╝██╔══██╗██╔════╝      ║
║             ██████╔╝█████╗     ██║   ██████╔╝██║           ║
║             ██╔══██╗██╔══╝     ██║   ██╔══██╗██║           ║
║             ██║  ██║███████╗   ██║   ██║  ██║╚██████╗      ║
║             ╚═╝  ╚═╝╚══════╝   ╚═╝   ╚═╝  ╚═╝ ╚═════╝      ║
║                                                              ║
║              O C R   /   T R A N S L A T O R               ║
║                    VERSION 1.994                            ║
╚══════════════════════════════════════════════════════════════╝
</pre>

</div>
""", unsafe_allow_html=True)


st.markdown("""
<div class="retro-box">

<span class="system-text">
SYSTEM STATUS: ONLINE ████████████████████ 100%
</span>

<br>

<span class="retro-small">
>> Inicializando módulo OCR... OK<br>
>> Inicializando módulo TRANSLATOR... OK<br>
>> Inicializando módulo TEXT-TO-SPEECH... OK<br>
>> Sistema listo para recibir información.
</span>

</div>
""", unsafe_allow_html=True)


# ============================================================
# TÍTULO
# ============================================================

st.title("RECONOCIMIENTO ÓPTICO DE CARACTERES")

st.subheader(
    "Elige la fuente de la imagen: CÁMARA / ARCHIVO"
)


# ============================================================
# DATOS INTERESANTES
# ============================================================

st.markdown("""
<div class="retro-box">

<b>╔══ ARCHIVO DE DATOS ══╗</b>

<br><br>

<b>OCR</b> significa <i>Optical Character Recognition</i>.
Esta tecnología permite convertir letras presentes en una
imagen en texto digital.

<br><br>

<b>¿SABÍAS QUE?</b>

<br>

• Tesseract es uno de los motores OCR de código abierto
  más conocidos.

<br>

• El OCR puede reconocer documentos fotografiados,
  carteles, libros y manuscritos dependiendo de la calidad.

<br>

• La calidad de iluminación y el contraste afectan
  directamente al reconocimiento.

<br>

• Una imagen con texto nítido normalmente produce
  mejores resultados que una fotografía borrosa.

<br><br>

<b>MEMORIA DEL SISTEMA:</b> 640 KB*<br>
<b>CPU:</b> RETRO-8086 EMULATED<br>
<b>MODE:</b> TEXT PROCESSING

<br><br>

<span class="retro-small">
* La referencia a 640 KB es un guiño a los computadores
personales clásicos de la época.
</span>

</div>
""", unsafe_allow_html=True)


# ============================================================
# SELECCIÓN DE CÁMARA
# ============================================================

cam_ = st.checkbox("📹 USAR CÁMARA")


if cam_:

    img_file_buffer = st.camera_input(
        "TOMA UNA FOTO"
    )

else:

    img_file_buffer = None


# ============================================================
# SIDEBAR - PROCESAMIENTO
# ============================================================

with st.sidebar:

    st.markdown("""
    <div class="display">
    ┌──────────────────────────┐<br>
    │ CAMERA PROCESSING UNIT   │<br>
    └──────────────────────────┘
    </div>
    """, unsafe_allow_html=True)

    st.subheader("Procesamiento para Cámara")

    filtro = st.radio(
        "Filtro para imagen con cámara",
        ("Sí", "No")
    )


# ============================================================
# CARGAR IMAGEN
# ============================================================

bg_image = st.file_uploader(
    "📁 CARGAR IMAGEN:",
    type=["png", "jpg"]
)


if bg_image is not None:

    uploaded_file = bg_image

    st.image(
        uploaded_file,
        caption="Imagen cargada.",
        use_container_width=True
    )

    # Guardar la imagen
    with open(uploaded_file.name, 'wb') as f:

        f.write(uploaded_file.read())

    st.success(
        f"Imagen guardada como {uploaded_file.name}"
    )

    # Leer imagen
    img_cv = cv2.imread(
        f'{uploaded_file.name}'
    )

    img_rgb = cv2.cvtColor(
        img_cv,
        cv2.COLOR_BGR2RGB
    )

    # OCR
    text = pytesseract.image_to_string(
        img_rgb
    )


# ============================================================
# MOSTRAR TEXTO DETECTADO
# ============================================================

st.markdown("""
<div class="terminal">

>> OCR OUTPUT
>> ------------------------------
</div>
""", unsafe_allow_html=True)

st.write(text)


# ============================================================
# INFORMACIÓN DEL TEXTO
# ============================================================

if text.strip():

    palabras = len(text.split())
    caracteres = len(text)
    lineas = len(text.splitlines())

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "PALABRAS",
            palabras
        )

    with col2:
        st.metric(
            "CARACTERES",
            caracteres
        )

    with col3:
        st.metric(
            "LÍNEAS",
            lineas
        )

    st.markdown("""
    <div class="retro-box">

    <b>ANÁLISIS DEL DOCUMENTO</b>

    <br><br>

    El sistema ha encontrado información textual
    en la imagen.

    <br><br>

    Estos datos son estimaciones obtenidas directamente
    del resultado producido por el motor OCR.

    </div>
    """, unsafe_allow_html=True)


# ============================================================
# CÁMARA
# ============================================================

if img_file_buffer is not None:

    # Leer buffer
    bytes_data = img_file_buffer.getvalue()

    cv2_img = cv2.imdecode(
        np.frombuffer(bytes_data, np.uint8),
        cv2.IMREAD_COLOR
    )

    # Aplicar filtro
    if filtro == 'Sí':

        cv2_img = cv2.bitwise_not(
            cv2_img
        )

    else:

        cv2_img = cv2_img

    img_rgb = cv2.cvtColor(
        cv2_img,
        cv2.COLOR_BGR2RGB
    )

    # OCR
    text = pytesseract.image_to_string(
        img_rgb
    )

    st.markdown("""
    <div class="terminal">

    >> CAMERA INPUT RECEIVED<br>
    >> IMAGE PROCESSING...<br>
    >> OCR SCANNING...<br>
    >> COMPLETE.

    </div>
    """, unsafe_allow_html=True)

    st.write(text)

    # Estadísticas
    if text.strip():

        palabras = len(text.split())
        caracteres = len(text)
        lineas = len(text.splitlines())

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "PALABRAS",
                palabras
            )

        with col2:
            st.metric(
                "CARACTERES",
                caracteres
            )

        with col3:
            st.metric(
                "LÍNEAS",
                lineas
            )


# ============================================================
# TRADUCCIÓN
# ============================================================

with st.sidebar:

    st.markdown("---")

    st.markdown("""
    <div class="display">
    ┌──────────────────────────┐<br>
    │ TRANSLATION MODULE       │<br>
    └──────────────────────────┘
    </div>
    """, unsafe_allow_html=True)

    st.subheader(
        "Parámetros de traducción"
    )

    try:
        os.mkdir("temp")
    except:
        pass

    translator = Translator()


    # ========================================================
    # IDIOMA DE ENTRADA
    # ========================================================

    in_lang = st.selectbox(
        "Seleccione el lenguaje de entrada",
        (
            "Ingles",
            "Español",
            "Bengali",
            "koreano",
            "Mandarin",
            "Japones"
        ),
    )


    if in_lang == "Ingles":
        input_language = "en"

    elif in_lang == "Español":
        input_language = "es"

    elif in_lang == "Bengali":
        input_language = "bn"

    elif in_lang == "koreano":
        input_language = "ko"

    elif in_lang == "Mandarin":
        input_language = "zh-cn"

    elif in_lang == "Japones":
        input_language = "ja"


    # ========================================================
    # IDIOMA DE SALIDA
    # ========================================================

    out_lang = st.selectbox(
        "Select your output language",
        (
            "Ingles",
            "Español",
            "Bengali",
            "koreano",
            "Mandarin",
            "Japones"
        ),
    )


    if out_lang == "Ingles":
        output_language = "en"

    elif out_lang == "Español":
        output_language = "es"

    elif out_lang == "Bengali":
        output_language = "bn"

    elif out_lang == "koreano":
        output_language = "ko"

    elif out_lang == "Mandarin":
        output_language = "zh-cn"

    elif out_lang == "Japones":
        output_language = "ja"


    # ========================================================
    # ACENTO
    # ========================================================

    english_accent = st.selectbox(
        "Seleccione el acento",
        (
            "Default",
            "India",
            "United Kingdom",
            "United States",
            "Canada",
            "Australia",
            "Ireland",
            "South Africa",
        ),
    )


    if english_accent == "Default":

        tld = "com"

    elif english_accent == "India":

        tld = "co.in"

    elif english_accent == "United Kingdom":

        tld = "co.uk"

    elif english_accent == "United States":

        tld = "com"

    elif english_accent == "Canada":

        tld = "ca"

    elif english_accent == "Australia":

        tld = "com.au"

    elif english_accent == "Ireland":

        tld = "ie"

    elif english_accent == "South Africa":

        tld = "co.za"


    # ========================================================
    # MOSTRAR TEXTO
    # ========================================================

    display_output_text = st.checkbox(
        "Mostrar texto"
    )


    # ========================================================
    # BOTÓN CONVERTIR
    # ========================================================

    if st.button("CONVERT"):

        result, output_text = text_to_speech(
            input_language,
            output_language,
            text,
            tld
        )

        audio_file = open(
            f"temp/{result}.mp3",
            "rb"
        )

        audio_bytes = audio_file.read()

        st.markdown(
            "## Tu audio:"
        )

        st.audio(
            audio_bytes,
            format="audio/mp3",
            start_time=0
        )


        if display_output_text:

            st.markdown(
                "## Texto de salida:"
            )

            st.write(
                f" {output_text}"
            )


# ============================================================
# INFORMACIÓN FINAL
# ============================================================

st.markdown("---")

st.markdown("""
<div class="terminal">

╔══════════════════════════════════════════════════════════╗
║                 SYSTEM INFORMATION                      ║
╠══════════════════════════════════════════════════════════╣
║                                                          ║
║  OCR ENGINE ............... TESSERACT                   ║
║  IMAGE PROCESSOR .......... OPENCV                      ║
║  TRANSLATOR ............... GOOGLE TRANSLATE            ║
║  VOICE ENGINE ............. gTTS                        ║
║                                                          ║
║  INPUT .................... IMAGE / CAMERA              ║
║  OUTPUT ................... TEXT / AUDIO                ║
║                                                          ║
║  STATUS ................... READY                       ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝

[ RETRO TRANSLATOR 1994 ]
[ ALL SYSTEMS OPERATIONAL ]

</div>
""", unsafe_allow_html=True)


st.markdown("""
<div class="retro-box">

<b>💾 ¿CÓMO FUNCIONA ESTE SISTEMA?</b>

<br><br>

<b>01.</b> Se obtiene una imagen mediante cámara o archivo.

<br><br>

<b>02.</b> OpenCV procesa la imagen.

<br><br>

<b>03.</b> Tesseract analiza los caracteres y genera texto.

<br><br>

<b>04.</b> Google Translate convierte el texto al idioma seleccionado.

<br><br>

<b>05.</b> gTTS transforma la traducción en audio.

<br><br>

<b>RESULTADO:</b> Imagen → OCR → Traducción → Voz

</div>
""", unsafe_allow_html=True)

 
    
    
