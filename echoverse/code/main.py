import streamlit as st
import base64
import io
from pathlib import Path
from pypdf import PdfReader
from model import genrate_reader_json
from utils import concated_text

# ---------------------------
# Configure page
# ---------------------------
st.set_page_config(
    page_title="EchoVerse - Turn Your Words Into Immersive Audio",
    page_icon="🎵",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# ---------------------------
# Load custom CSS
# ---------------------------
def load_css():
    st.markdown(
        """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    .stApp { 
        background: linear-gradient(135deg, #0f4c75 0%, #3282b8 100%); 
        font-family: 'Inter', sans-serif; 
    }
    #MainMenu, footer, header {visibility: hidden;}
    
    .main-header { 
        text-align: center; 
        padding: 2rem 0; 
        margin-bottom: 2rem; 
    }
    .logo-text { 
        font-size: 2.5rem; 
        font-weight: 700; 
        color: white; 
        margin-bottom: 0.5rem; 
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3); 
    }
    .tagline { 
        font-size: 1.2rem; 
        color: #d9d9d9; 
        font-weight: 300; 
        margin-bottom: 0; 
    }

    .input-container { 
        background: rgba(255, 255, 255, 0.95); 
        border-radius: 20px; 
        padding: 2rem; 
        margin: 2rem 0; 
        box-shadow: 0 10px 30px rgba(0,0,0,0.2); 
    }

    .stTextArea textarea { 
        background-color: #f8f9fa !important; 
        color: black !important;
        border: 2px solid #3282b8 !important; 
        border-radius: 15px !important; 
        padding: 1rem !important; 
        font-size: 16px !important; 
        min-height: 200px !important; 
    }

    .stFileUploader { 
        background-color: #d9d9d9; 
        border-radius: 15px; 
        padding: 2rem; 
        text-align: center; 
        border: 2px dashed #3282b8; 
        transition: all 0.3s ease; 
    }

    .stButton button { 
        background: linear-gradient(135deg, #0f4c75, #3282b8) !important; 
        color: white !important; 
        border: none !important; 
        border-radius: 25px !important; 
        padding: 0.75rem 2rem !important; 
        font-size: 18px !important; 
        font-weight: 600 !important; 
        width: 100% !important; 
    }

    .content-card { 
        background: rgba(255, 255, 255, 0.95); 
        border-radius: 15px; 
        padding: 1.5rem; 
        margin-bottom: 1rem; 
        box-shadow: 0 5px 15px rgba(0,0,0,0.1); 
        height: 400px; 
        overflow-y: auto; 
    }

    .card-title { 
        font-size: 1.3rem; 
        font-weight: 600; 
        color: #1b262c; 
        margin-bottom: 1rem; 
        border-bottom: 2px solid #3282b8; 
        padding-bottom: 0.5rem; 
    }
    </style>
    """,
        unsafe_allow_html=True,
    )


load_css()


# ---------------------------
# Header Renderer
# ---------------------------
def render_header(show_back_button=False):
    if show_back_button:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col1:
            if st.button("← Back", key="back_btn", help="Return to home"):
                st.session_state.page = "home"
                st.rerun()
        with col2:
            st.markdown(
                '<div class="main-header"><h1 class="logo-text">🎵 EchoVerse</h1></div>',
                unsafe_allow_html=True,
            )
    else:
        st.markdown(
            '<div class="main-header"><h1 class="logo-text">🎵 EchoVerse</h1><p class="tagline">Turn Your Words Into Immersive Audio</p></div>',
            unsafe_allow_html=True,
        )


# ---------------------------
# Home Page
# ---------------------------
def render_home_page():
    render_header()

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(
            '<div class="card-title" style="color:white;">📝 Text Input</div>',
            unsafe_allow_html=True,
        )
        text_input = st.text_area(
            "Enter your text",
            placeholder="Paste your text here...",
            height=200,
            key="text_input",
            label_visibility="collapsed",
        )

    with col2:
        st.markdown(
            '<div class="card-title" style="color:white;">📄 Upload PDF</div>',
            unsafe_allow_html=True,
        )
        uploaded_file = st.file_uploader(
            "Upload file",
            type=["pdf", "txt"],
            help="Upload a PDF or TXT file",
            label_visibility="collapsed",
        )
        if uploaded_file:
            st.success(f"✅ File uploaded: {uploaded_file.name}")

    col1, col2 = st.columns([1, 2], gap="small", vertical_alignment="bottom")
    with col1:
        tone = st.selectbox(
            "Select Tone",
            [
                "Neutral",
                "Suspenseful",
                "Inspiring",
                "Professional",
                "Casual",
                "Dramatic",
            ],
            key="tone_select",
        )

    with col2:
        if st.button("🎵 Generate Audio", key="generate_btn", type="primary"):
            extracted_text = ""

            if text_input.strip():
                extracted_text = text_input.strip()
                st.success("✅ Text input received successfully!")

            elif uploaded_file:
                st.info("📄 Extracting text from uploaded file...")
                if uploaded_file.type == "application/pdf":
                    try:
                        reader = PdfReader(uploaded_file)
                        text = ""
                        for page in reader.pages:
                            text += page.extract_text()
                        extracted_text = " ".join(text.split("\n"))
                        st.success("✅ File text extracted successfully!")
                    except Exception as e:
                        st.error(f"❌ Error extracting PDF: {e}")
                        return

                elif uploaded_file.type == "text/plain":
                    extracted_text = uploaded_file.read().decode("utf-8")
                    st.success("✅ File text extracted successfully!")
                else:
                    st.error("Currently, only PDF and TXT are supported.")
                    return

                if not extracted_text.strip():
                    st.error("⚠️ No text found in uploaded file.")
                    return
            else:
                st.error("Please provide text input or upload a file!")
                return

            st.session_state.original_text = extracted_text
            st.session_state.selected_tone = tone
            st.session_state.page = "output"
            st.rerun()


# ---------------------------
# Output Page
# ---------------------------
def render_output_page():
    render_header(show_back_button=True)
    col1, col2, col3 = st.columns([1, 1.5, 1])

    with col1:
        original_text = st.session_state.get("original_text", "No text provided")
        st.markdown(
            f"<div class='content-card'><div class='card-title'>📄 Original Input</div><div style='color: #1b262c; line-height: 1.6; font-size: 14px;'>{original_text}</div></div>",
            unsafe_allow_html=True,
        )

    with col2:
        tone = st.session_state.get("selected_tone", "Neutral")
        ai_generated_object = genrate_reader_json(
            st.session_state.get("original_text", "No text provided"), tone
        )
        print(ai_generated_object)
        adapted_text = concated_text(ai_generated_object)
        st.markdown(
            f"<div class='content-card'><div class='card-title'>🎵 Tone-Adapted Narration</div><div style='color: #1b262c; line-height: 1.6; font-size: 14px; overflow-y: scroll;'>{adapted_text}</div></div>",
            unsafe_allow_html=True,
        )

    with col3:
        st.markdown(
            '<div class="content-card"><div class="card-title">🎧 Audio Player</div>',
            unsafe_allow_html=True,
        )
        st.info(
            "Audio generation feature is enabled in backend. Your tone-adapted audio will play here once ready."
        )


# ---------------------------
# Page Router
# ---------------------------
if "page" not in st.session_state:
    st.session_state.page = "home"

if st.session_state.page == "home":
    render_home_page()
elif st.session_state.page == "output":
    render_output_page()
