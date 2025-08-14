#this is old UI code

# import streamlit as st

# import base64
# import io
# from pathlib import Path
# from pypdf import PdfReader



# # Configure page
# st.set_page_config(
#     page_title="EchoVerse - Turn Your Words Into Immersive Audio",
#     page_icon="🎵",
#     layout="wide",
#     initial_sidebar_state="collapsed"
# )

# # Custom CSS for EchoVerse styling
# def load_css():
#     st.markdown("""<style>
#     @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
#     .stApp { background: linear-gradient(135deg, #0f4c75 0%, #3282b8 100%); font-family: 'Inter', sans-serif; }
#     #MainMenu, footer, header {visibility: hidden;}
#     .main-header { text-align: center; padding: 2rem 0; margin-bottom: 2rem; }
#     .logo-text { font-size: 2.5rem; font-weight: 700; color: white; margin-bottom: 0.5rem; text-shadow: 2px 2px 4px rgba(0,0,0,0.3); }
#     .tagline { font-size: 1.2rem; color: #d9d9d9; font-weight: 300; margin-bottom: 0; }
#     .input-container { background: rgba(255, 255, 255, 0.95); border-radius: 20px; padding: 2rem; margin: 2rem 0; box-shadow: 0 10px 30px rgba(0,0,0,0.2); }
#     .stTextArea textarea { background-color: #f8f9fa !important; border: 2px solid #3282b8 !important; border-radius: 15px !important; padding: 1rem !important; font-size: 16px !important; min-height: 200px !important; }
#     .stFileUploader { background-color: #d9d9d9; border-radius: 15px; padding: 2rem; text-align: center; border: 2px dashed #3282b8; transition: all 0.3s ease; }
#     .stButton button { background: linear-gradient(135deg, #0f4c75, #3282b8) !important; color: white !important; border: none !important; border-radius: 25px !important; padding: 0.75rem 2rem !important; font-size: 18px !important; font-weight: 600 !important; width: 100% !important; }
#     .content-card { background: rgba(255, 255, 255, 0.95); border-radius: 15px; padding: 1.5rem; margin-bottom: 1rem; box-shadow: 0 5px 15px rgba(0,0,0,0.1); height: 400px; overflow-y: auto; }
#     .card-title { font-size: 1.3rem; font-weight: 600; color: #1b262c; margin-bottom: 1rem; border-bottom: 2px solid #3282b8; padding-bottom: 0.5rem; }
#     </style>""", unsafe_allow_html=True)

# # Header Renderer
# def render_header(show_back_button=False):
#     if show_back_button:
#         col1, col2, col3 = st.columns([1, 2, 1])
#         with col1:
#             if st.button("← Back", key="back_btn", help="Return to home"):
#                 st.session_state.page = "home"
#                 st.rerun()
#         with col2:
#             st.markdown('<div class="main-header"><h1 class="logo-text">🎵 EchoVerse</h1></div>', unsafe_allow_html=True)
#     else:
#         st.markdown('<div class="main-header"><h1 class="logo-text">🎵 EchoVerse</h1><p class="tagline">Turn Your Words Into Immersive Audio</p></div>', unsafe_allow_html=True)

# # PDF extraction using Docling

# def extract_text_with_docling(uploaded_file):
#     try:
#         # Save uploaded file to a temporary location
#         with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
#             tmp_file.write(uploaded_file.read())
#             tmp_path = Path(tmp_file.name)

#         converter = DocumentConverter()
#         result = converter.convert(tmp_path)

#         # Clean up temp file if needed
#         tmp_path.unlink(missing_ok=True)

#         return result.document.export_to_text()
#     except Exception as e:
#         st.error(f"❌ Error extracting PDF: {e}")
#         return ""


# # Home Page
# def render_home_page():
#     render_header()

#     st.markdown('<div class="input-container">', unsafe_allow_html=True)
#     col1, col2 = st.columns(2)

#     with col1:
#         st.markdown('<div class="card-title">📝 Text Input</div>', unsafe_allow_html=True)
#         text_input = st.text_area(
#             "Enter your text",  # added non-empty label for Streamlit warning
#             placeholder="Paste your text here...",
#             height=200,
#             key="text_input",
#             label_visibility="collapsed"
#         )

#     with col2:
#         st.markdown('<div class="card-title">📄 Upload PDF</div>', unsafe_allow_html=True)
#         uploaded_file = st.file_uploader(
#             "Upload file",  # added label to fix accessibility warning
#             type=['pdf', 'txt'],
#             help="Upload a PDF or TXT file",
#             label_visibility="collapsed"
#         )
#         if uploaded_file:
#             st.success(f"✅ File uploaded: {uploaded_file.name}")

#     st.markdown("</div>", unsafe_allow_html=True)

#     col1, col2 = st.columns([1, 2])
#     with col1:
#         tone = st.selectbox(
#             "Select Tone",
#             ["Neutral", "Suspenseful", "Inspiring", "Professional", "Casual", "Dramatic"],
#             key="tone_select"
#         )

#     with col2:
#         if st.button("🎵 Generate Audio", key="generate_btn", type="primary"):
#             extracted_text = ""

#             if text_input.strip():
#                 extracted_text = text_input.strip()
#                 print("\n📌 Pasted Text:\n", extracted_text)  # debug print
#                 st.success("✅ Text input received successfully!")

#             elif uploaded_file:
#                 st.info("📄 Extracting text from uploaded file...")
#                 if uploaded_file.type == "application/pdf":
#                     try:
#                         from docling.document_converter import DocumentConverter
#                         import tempfile

#                         # Save uploaded file to a temporary file
#                         with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
#                             tmp_file.write(uploaded_file.read())
#                             tmp_path = tmp_file.name

#                         # converter = DocumentConverter()
#                         # result = converter.convert(tmp_path)
#                         # extracted_text = result.document.export_to_text()
#                         reader = PdfReader(tmp_path)
#                         text = ""
#                         for page in reader.pages:
#                             text+=page.extract_text()
#                         print(text)


#                         print("\n📌 PDF Extracted Text:\n", text)  # debug print
#                         st.success("✅ File text extracted successfully!")
#                     except Exception as e:
#                         st.error(f"❌ Error extracting PDF: {e}")
#                         return

#                 elif uploaded_file.type == "text/plain":
#                     extracted_text = uploaded_file.read().decode("utf-8")
#                     print("\n📌 TXT Extracted Text:\n", extracted_text)  # debug print
#                     st.success("✅ File text extracted successfully!")

#                 else:
#                     st.error("Currently, only PDF and TXT are supported.")
#                     return

#                 if not extracted_text.strip():
#                     st.error("⚠️ No text found in uploaded file.")
#                     return

#             else:
#                 st.error("Please provide text input or upload a file!")
#                 return

#             # Store in session for further processing
#             st.session_state.original_text = extracted_text
#             st.session_state.selected_tone = tone
#             st.session_state.page = "output"
#             st.rerun()


# # Output Page
# def render_output_page():
#     render_header(show_back_button=True)
#     col1, col2, col3 = st.columns([1, 1.5, 1])

#     with col1:
#         st.markdown('<div class="content-card"><div class="card-title">📄 Original Input</div>', unsafe_allow_html=True)
#         original_text = st.session_state.get('original_text', 'No text provided')
#         st.markdown(f"<div style='color: #1b262c; line-height: 1.6; font-size: 14px;'>{original_text}</div></div>", unsafe_allow_html=True)

#     with col2:
#         st.markdown('<div class="content-card"><div class="card-title">🎵 Tone-Adapted Narration</div>', unsafe_allow_html=True)
#         tone = st.session_state.get('selected_tone', 'Neutral')
#         adapted_text = f"""
#         [Adapted for {tone} tone]

#         This is your original content, now enhanced and optimized for {tone.lower()} delivery.
#         The text has been carefully restructured to match the selected emotional tone while
#         preserving the core message and meaning.

#         Key adaptations include:
#         • Adjusted pacing and rhythm
#         • Enhanced emotional resonance
#         • Optimized for audio delivery
#         • Tone-specific vocabulary choices
#         """
#         st.markdown(f"<div style='color: #1b262c; line-height: 1.6; font-size: 14px; margin-bottom: 1rem;'>{adapted_text}</div></div>", unsafe_allow_html=True)

#     with col3:
#         st.markdown('<div class="card-title">⚡ Actions</div>', unsafe_allow_html=True)
#         if st.button("📥 Download MP3"):
#             st.success("🎵 Audio file ready for download!")
#             st.balloons()

# # Main App
# def main():
#     load_css()
#     if 'page' not in st.session_state:
#         st.session_state.page = "home"
#     if st.session_state.page == "home":
#         render_home_page()
#     elif st.session_state.page == "output":
#         render_output_page()

# if __name__ == "__main__":
#     main()
