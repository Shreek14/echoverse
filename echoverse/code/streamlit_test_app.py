import streamlit as st
import base64
import io
from pathlib import Path

# Configure page
st.set_page_config(
    page_title="EchoVerse - Turn Your Words Into Immersive Audio",
    page_icon="🎵",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for EchoVerse styling


def load_css():
    st.markdown("""
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global Styles */
    .stApp {
        background: linear-gradient(135deg, #0f4c75 0%, #3282b8 100%);
        font-family: 'Inter', sans-serif;
    }
    
    .block-container {
        padding-top: 0.25rem;
        padding-bottom: 0.25rem;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Custom Header */
    .main-header {
        text-align: center;
        padding: 1rem 0;
        margin-bottom: 1rem;
    }
    
    .logo-text {
        font-size: 2.3rem;
        font-weight: 700;
        color: white;
        margin-bottom: 0.25rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .tagline {
        font-size: 1.1rem;
        color: #d9d9d9;
        font-weight: 300;
        margin-bottom: 0;
    }
    
    /* Input Area Styling */
    .input-container {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 20px;
        padding: 1rem;
        margin: 1rem 0;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    }
    
    /* Text Area Styling */
    .stTextArea textarea {
        background-color: #f8f9fa !important;
        border: 2px solid #3282b8 !important;
        border-radius: 15px !important;
        padding: 0.75rem !important;
        font-size: 15px !important;
        min-height: 180px !important;
    }
    
    .stTextArea textarea:focus {
        border-color: #0f4c75 !important;
        box-shadow: 0 0 10px rgba(50, 130, 184, 0.3) !important;
    }
    
    /* File Uploader Styling */
    .stFileUploader {
        background-color: #d9d9d9;
        border-radius: 15px;
        padding: 1rem;
        text-align: center;
        border: 2px dashed #3282b8;
        transition: all 0.3s ease;
    }
    
    .stFileUploader:hover {
        background-color: #e8f4f8;
        border-color: #0f4c75;
    }
    
    /* Button Styling */
    .stButton button {
        background: linear-gradient(135deg, #0f4c75, #3282b8) !important;
        color: white !important;
        border: none !important;
        border-radius: 25px !important;
        padding: 0.5rem 1.5rem !important;
        font-size: 16px !important;
        font-weight: 600 !important;
        width: 100% !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(15, 76, 117, 0.3) !important;
    }
    
    .stButton button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(15, 76, 117, 0.4) !important;
    }
    
    /* Selectbox Styling */
    .stSelectbox select {
        background-color: #f8f9fa !important;
        border: 2px solid #d9d9d9 !important;
        border-radius: 10px !important;
        padding: 0.5rem !important;
        font-size: 16px !important;
    }
    
    /* Output Page Styling */
    .output-header {
        background: rgba(255, 255, 255, 0.1);
        padding: 1rem 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }
    
    .back-button {
        background: #d9d9d9 !important;
        color: #1b262c !important;
        border: none !important;
        border-radius: 20px !important;
        padding: 0.5rem 1.5rem !important;
        font-weight: 500 !important;
    }
    
    .content-card {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 15px;
        padding: 1rem;
        margin-bottom: 0.5rem;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        height: 350px;
        overflow-y: auto;
    }
    
    .card-title {
        font-size: 1.2rem;
        font-weight: 600;
        color: #1b262c;
        margin-bottom: 0.5rem;
        border-bottom: 2px solid #3282b8;
        padding-bottom: 0.25rem;
    }
    
    .audio-player {
        background: #0f4c75;
        border-radius: 15px;
        padding: 1.5rem;
        margin-top: 1rem;
        color: white;
    }
    
    .action-buttons {
        display: flex;
        flex-direction: column;
        gap: 1rem;
    }
    
    .action-button {
        background: #d9d9d9 !important;
        color: #1b262c !important;
        border: none !important;
        border-radius: 15px !important;
        padding: 1rem !important;
        font-weight: 500 !important;
        transition: all 0.3s ease !important;
    }
    
    .action-button:hover {
        background: #3282b8 !important;
        color: white !important;
    }
    
    .download-button {
        background: linear-gradient(135deg, #0f4c75, #3282b8) !important;
        color: white !important;
        font-size: 18px !important;
        font-weight: 600 !important;
    }
    
    /* Footer */
    .custom-footer {
        text-align: center;
        padding: 1rem 0;
        color: #d9d9d9;
        font-size: 0.9rem;
        margin-top: 0.5rem;
    }
    
    /* Responsive Design */
    @media (max-width: 768px) {
        .logo-text {
            font-size: 2rem;
        }
        
        .tagline {
            font-size: 1rem;
        }
        
        .input-container {
            padding: 1rem;
            margin: 1rem 0;
        }
        
        .content-card {
            height: 300px;
        }
    }
    
    /* Loading Animation */
    .loading-spinner {
        display: inline-block;
        width: 20px;
        height: 20px;
        border: 3px solid #f3f3f3;
        border-top: 3px solid #3282b8;
        border-radius: 50%;
        animation: spin 1s linear infinite;
    }
    
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    /* Progress Bar */
    .progress-container {
        background-color: rgba(255, 255, 255, 0.2);
        border-radius: 10px;
        padding: 0.5rem;
        margin: 1rem 0;
    }
    
    .progress-bar {
        background: linear-gradient(90deg, #3282b8, #0f4c75);
        height: 8px;
        border-radius: 5px;
        transition: width 0.3s ease;
    }
    </style>
    """, unsafe_allow_html=True)


def render_header(show_back_button=False):
    if show_back_button:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col1:
            if st.button("← Back", key="back_btn", help="Return to home"):
                st.session_state.page = "home"
                st.rerun()
        with col2:
            st.markdown("""
            <div class="main-header">
                <h1 class="logo-text">🎵 EchoVerse</h1>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="main-header">
            <h1 class="logo-text">🎵 EchoVerse</h1>
            <p class="tagline">Turn Your Words Into Immersive Audio</p>
        </div>
        """, unsafe_allow_html=True)


def render_home_page():
    render_header()

    # Main input container
    st.markdown('<div class="input-container">', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="card-title">📝 Text Input</div>',
                    unsafe_allow_html=True)
        text_input = st.text_area(
            "",
            placeholder="Paste your text here...",
            height=200,
            key="text_input",
            label_visibility="collapsed"
        )

        st.markdown('<div class="card-title">📄 Upload PDF</div>',
                    unsafe_allow_html=True)
        uploaded_file = st.file_uploader(
            "",
            type=['pdf', 'txt', 'docx'],
            help="Upload a PDF, TXT, or DOCX file",
            label_visibility="collapsed"
        )
        if uploaded_file:
            st.success(f"✅ File uploaded: {uploaded_file.name}")

    with col2:
        st.markdown('<div class="card-title">🎯 Tone Selection</div>',
                    unsafe_allow_html=True)
        tone = st.selectbox(
            "",
            ["Neutral", "Suspenseful", "Inspiring",
                "Professional", "Casual", "Dramatic"],
            key="tone_select"
        )
        st.markdown('<br>', unsafe_allow_html=True)
        if st.button("🎵 Generate Audio", key="generate_btn", type="primary"):
            if text_input or uploaded_file:
                # Store data in session state
                st.session_state.original_text = text_input if text_input else f"Content from {uploaded_file.name}"
                st.session_state.selected_tone = tone
                st.session_state.page = "output"

                # Show loading animation
                with st.spinner("🎵 Generating your immersive audio experience..."):
                    import time
                    time.sleep(2)  # Simulate processing time

                st.rerun()
            else:
                st.error("Please provide text input or upload a file!")

    # Footer
    st.markdown("""
    <div class="custom-footer">
        Powered by IBM Watsonx & EchoVerse AI
    </div>
    """, unsafe_allow_html=True)


def render_output_page():
    render_header(show_back_button=True)

    # Three column layout
    col1, col2, col3 = st.columns([1, 1, 0.5])

    with col1:

        original_text = st.session_state.get(
            'original_text', 'No text provided')
        st.markdown(f"""
            <div class="content-card">
            <div class="card-title">📄 Original Input</div><div style="color: #1b262c; line-height: 1.6; font-size: 14px;">
                {original_text}
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col2:

        # Generate sample adapted text based on tone
        tone = st.session_state.get('selected_tone', 'Neutral')
        adapted_text = f"""
        [Adapted for {tone} tone]
        
        This is your original content, now enhanced and optimized for {tone.lower()} delivery. 
        The text has been carefully restructured to match the selected emotional tone while 
        preserving the core message and meaning.
        
        Key adaptations include:
        • Adjusted pacing and rhythm
        • Enhanced emotional resonance
        • Optimized for audio delivery
        • Tone-specific vocabulary choices
        """

        st.markdown(f"""
                    <div class="content-card">
            <div class="card-title">🎵 Tone-Adapted Narration</div>
            <div style="color: #1b262c; line-height: 1.6; font-size: 14px; margin-bottom: 1rem;">
                {adapted_text}
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Audio Player
        st.markdown("""
        <div class="audio-player">
            <div style="display: flex; align-items: center; gap: 1rem; margin-bottom: 1rem;">
                <button style="background: #d9d9d9; border: none; border-radius: 50%; width: 50px; height: 50px; cursor: pointer;">
                    ▶️
                </button>
                <button style="background: #d9d9d9; border: none; border-radius: 25%; padding: 0.5rem; cursor: pointer;">
                    ⏪ 10s
                </button>
                <div style="flex: 1; color: white;">
                    <div style="background: rgba(255,255,255,0.2); height: 6px; border-radius: 3px; margin-bottom: 0.5rem;">
                        <div style="background: #d9d9d9; height: 100%; width: 30%; border-radius: 3px;"></div>
                    </div>
                    <small>1:23 / 4:56</small>
                </div>
                <div style="display: flex; align-items: center; gap: 0.5rem;">
                    🔊
                    <div style="background: rgba(255,255,255,0.2); height: 4px; width: 60px; border-radius: 2px;">
                        <div style="background: #d9d9d9; height: 100%; width: 70%; border-radius: 2px;"></div>
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown('<div class="card-title">⚡ Actions</div>',
                    unsafe_allow_html=True)

        # Regenerate with different tone
        if st.button("🔄 Regenerate", key="regenerate_btn", help="Generate with different settings"):
            new_tone = st.selectbox(
                "Choose new tone:",
                ["Neutral", "Suspenseful", "Inspiring",
                    "Professional", "Casual", "Dramatic"],
                key="new_tone_select"
            )
            if st.button("Apply New Tone", key="apply_tone"):
                st.session_state.selected_tone = new_tone
                st.rerun()

        st.markdown('<hr style="margin:0.5rem 0;">', unsafe_allow_html=True)

        # Translation
        st.markdown("🌍 **Translate**")
        language = st.selectbox(
            "",
            ["English", "Spanish", "French", "German",
                "Italian", "Portuguese", "Chinese", "Japanese"],
            key="language_select",
            label_visibility="collapsed"
        )

        if st.button("Translate", key="translate_btn"):
            st.success(f"✅ Translated to {language}")

        st.markdown('<hr style="margin:0.5rem 0;">', unsafe_allow_html=True)

        # Download
        if st.button("📥 Download MP3", key="download_btn", help="Download your audio file"):
            # Simulate file download
            st.success("🎵 Audio file ready for download!")
            st.balloons()

        # Additional actions
        st.markdown('<hr style="margin:0.5rem 0;">', unsafe_allow_html=True)

        if st.button("📋 Copy Text", key="copy_btn"):
            st.success("✅ Text copied to clipboard!")

        if st.button("📧 Share", key="share_btn"):
            st.info("🔗 Share link generated!")


def main():
    # Load custom CSS
    load_css()

    # Initialize session state
    if 'page' not in st.session_state:
        st.session_state.page = "home"

    # Route to appropriate page
    if st.session_state.page == "home":
        render_home_page()
    elif st.session_state.page == "output":
        render_output_page()


if __name__ == "__main__":
    main()
