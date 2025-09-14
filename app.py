# app.py - Complete version with Translation, TTS, File Upload, and Full UX Enhancements
import streamlit as st
import google.generativeai as genai
from gtts import gTTS  
import io  
from datetime import datetime
import pandas as pd
import PyPDF2
import docx
import re

# Validation functions
def validate_text_length(text, max_length=5000):
    """Validate text length for translation"""
    if not text or not text.strip():
        return False, "Please enter some text to translate"
    
    char_count = len(text.strip())
    if char_count > max_length:
        return False, f"Text is too long ({char_count:,} characters). Maximum allowed: {max_length:,} characters"
    
    if char_count < 3:
        return False, "Text is too short. Please enter at least 3 characters"
    
    return True, ""

def validate_api_key(api_key):
    """Validate API key format"""
    if not api_key or not api_key.strip():
        return False, "API key is required"
    
    # Basic format check for Google API key
    if not api_key.startswith('AIza'):
        return False, "Invalid API key format. Google API keys should start with 'AIza'"
    
    if len(api_key) < 30:
        return False, "API key appears to be incomplete"
    
    return True, ""

def detect_language_info(text):
    """Detect input language characteristics"""
    if not text:
        return "No text provided"
    
    # Simple language detection based on character patterns
    if re.search(r'[一-龯]', text):
        return "🇨🇳 Chinese characters detected"
    elif re.search(r'[あ-ん]|[ア-ン]|[ひ-ゞ]', text):
        return "🇯🇵 Japanese characters detected"
    elif re.search(r'[가-힣]', text):
        return "🇰🇷 Korean characters detected"
    elif re.search(r'[а-я]', text, re.IGNORECASE):
        return "🇷🇺 Cyrillic characters detected"
    elif re.search(r'[א-ת]', text):
        return "🇮🇱 Hebrew characters detected"
    elif re.search(r'[ا-ي]', text):
        return "🇸🇦 Arabic characters detected"
    elif re.search(r'[ñáéíóúü]', text, re.IGNORECASE):
        return "🇪🇸 Spanish characters detected"
    elif re.search(r'[àâäéèêëïîôöùûüÿç]', text, re.IGNORECASE):
        return "🇫🇷 French characters detected"
    elif re.search(r'[äöüß]', text, re.IGNORECASE):
        return "🇩🇪 German characters detected"
    else:
        return "🇺🇸 Latin characters detected"

def validate_file_size(file_size, max_size_mb=10):
    """Validate uploaded file size"""
    max_size_bytes = max_size_mb * 1024 * 1024
    if file_size > max_size_bytes:
        return False, f"File is too large ({file_size/1024/1024:.1f} MB). Maximum allowed: {max_size_mb} MB"
    return True, ""

def sanitize_filename(filename):
    """Create safe filename for downloads"""
    # Remove unsafe characters
    safe_name = re.sub(r'[<>:"/\\|?*]', '_', filename)
    # Remove extra spaces and dots
    safe_name = re.sub(r'[.\s]+', '_', safe_name)
    return safe_name[:50]  # Limit length

# Language configuration with TTS support
SUPPORTED_LANGUAGES = {
    "Spanish": {"code": "es", "native_name": "Español"},
    "French": {"code": "fr", "native_name": "Français"},
    "German": {"code": "de", "native_name": "Deutsch"},
    "Italian": {"code": "it", "native_name": "Italiano"},
    "Portuguese": {"code": "pt", "native_name": "Português"},
    "Russian": {"code": "ru", "native_name": "Русский"},
    "Japanese": {"code": "ja", "native_name": "日本語"},
    "Korean": {"code": "ko", "native_name": "한국어"},
    "Chinese": {"code": "zh", "native_name": "中文"},
    "Arabic": {"code": "ar", "native_name": "العربية"},
    "Hindi": {"code": "hi", "native_name": "हिन्दी"},
    "Dutch": {"code": "nl", "native_name": "Nederlands"},
    "Polish": {"code": "pl", "native_name": "Polski"},
    "Turkish": {"code": "tr", "native_name": "Türkçe"},
    "Swedish": {"code": "sv", "native_name": "Svenska"}
}

# Configure page
st.set_page_config(
    page_title="Universal Translator & TTS",
    page_icon="🌍",
    layout="wide"
)

# Title
st.title("🌍 Universal Text Translator & Speech Converter")
st.markdown("*Translate text into multiple languages and convert to speech*")

# Initialize session state
if 'translated_text' not in st.session_state:
    st.session_state.translated_text = ""
if 'current_language' not in st.session_state:
    st.session_state.current_language = ""
if 'audio_data' not in st.session_state:
    st.session_state.audio_data = None
if 'translation_count' not in st.session_state:
    st.session_state.translation_count = 0
if 'audio_count' not in st.session_state:
    st.session_state.audio_count = 0
if 'file_count' not in st.session_state:
    st.session_state.file_count = 0
if 'session_start' not in st.session_state:
    st.session_state.session_start = datetime.now()
if 'translation_attempts' not in st.session_state:
    st.session_state.translation_attempts = 0
if 'audio_attempts' not in st.session_state:
    st.session_state.audio_attempts = 0

# Sidebar for API key with enhanced validation
with st.sidebar:
    st.header("⚙️ Configuration")
    api_key = st.text_input("Enter Gemini API Key", type="password")
    
    if api_key:
        # Validate API key format
        is_valid, error_msg = validate_api_key(api_key)
        if is_valid:
            try:
                genai.configure(api_key=api_key)
                st.success("✅ API Key configured!")
            except Exception as e:
                st.error(f"❌ API key configuration failed: {str(e)}")
        else:
            st.error(f"❌ {error_msg}")
    
    # Enhanced usage statistics and tips (only show if API key is valid)
    if api_key and is_valid:
        st.markdown("---")
        st.subheader("📊 Session Statistics")
        
        # Main counters in a grid
        col1, col2 = st.columns(2)
        with col1:
            st.metric("🔤 Translations", st.session_state.translation_count)
            st.metric("📁 Files Processed", st.session_state.file_count)
        with col2:
            st.metric("🎵 Audio Files", st.session_state.audio_count)
            
            # Session duration
            session_duration = datetime.now() - st.session_state.session_start
            minutes = session_duration.seconds // 60
            st.metric("⏱️ Session Time", f"{minutes} min")
        
        # Success rates (if we have attempts)
        if st.session_state.translation_attempts > 0:
            translation_success_rate = (st.session_state.translation_count / st.session_state.translation_attempts) * 100
            st.metric("🎯 Translation Success", f"{translation_success_rate:.0f}%")
        
        if st.session_state.audio_attempts > 0:
            audio_success_rate = (st.session_state.audio_count / st.session_state.audio_attempts) * 100
            st.metric("🔊 Audio Success", f"{audio_success_rate:.0f}%")
        
        # Reset statistics button
        if st.button("🔄 Reset Statistics", help="Reset all session counters"):
            st.session_state.translation_count = 0
            st.session_state.audio_count = 0
            st.session_state.file_count = 0
            st.session_state.translation_attempts = 0
            st.session_state.audio_attempts = 0
            st.session_state.session_start = datetime.now()
            st.success("✅ Statistics reset!")
            st.rerun()

        # Usage tips
        with st.expander("💡 Usage Tips & Help"):
            st.markdown("""
            **🎯 For Best Results:**
            - Keep text under 1000 characters for faster processing
            - Use clear, simple language for better translations
            - PDF files work best when they contain selectable text
            - Try different languages to compare translation quality
            
            **🔧 Troubleshooting:**
            - If translation fails, try shorter text segments
            - For file uploads, ensure files aren't password-protected
            - Audio generation works best with shorter translated text
            - Some languages may have limited TTS voice quality
            
            **📝 Supported Features:**
            - **Translation**: 15+ languages via Google Gemini API
            - **File Types**: TXT, PDF, CSV, Excel, Word documents  
            - **Audio**: MP3 downloads with normal/slow speed options
            - **File Size**: Up to 10MB per file
            - **Text Length**: Up to 5000 characters per translation
            
            **🌟 Pro Tips:**
            - Use the language detection feature to identify input text
            - Download audio files for offline playback
            - Check session statistics to track your usage
            - Reset statistics to start fresh anytime
            """)

# Main interface
if api_key and validate_api_key(api_key)[0]:
    # INPUT METHOD SELECTION
    st.subheader("📝 Choose Input Method")
    input_method = st.radio(
        "How would you like to provide text?",
        ["✍️ Type text directly", "📁 Upload a file"],
        horizontal=True
    )
    
    input_text = ""
    
    if input_method == "✍️ Type text directly":
        # Direct text input
        input_text = st.text_area("Enter text to translate:", height=150, placeholder="Type your text here...")
        
        # Show character count for direct input
        if input_text:
            char_count = len(input_text)
            if char_count > 4000:
                st.warning(f"⚠️ {char_count:,} characters (approaching 5000 limit)")
            else:
                st.info(f"📝 {char_count:,} characters")
    
    else:
        # FILE UPLOAD METHOD
        st.markdown("**Supported file types:** TXT, PDF, CSV, Excel (.xlsx, .xls), Word (.docx)")
        
        uploaded_file = st.file_uploader(
            "Choose a file",
            type=['txt', 'pdf', 'csv', 'xlsx', 'xls', 'docx'],
            help="Upload a file to extract and translate its text content"
        )
        
        if uploaded_file is not None:
            # Show file info
            file_info = {
                "name": uploaded_file.name,
                "type": uploaded_file.type,
                "size": f"{uploaded_file.size / 1024:.1f} KB"
            }
            
            st.info(f"📄 **{file_info['name']}** ({file_info['type']}, {file_info['size']})")
            
            # Validate file size
            size_valid, size_error = validate_file_size(uploaded_file.size)
            if not size_valid:
                st.error(f"❌ {size_error}")
                input_text = ""
            else:
                # Extract text based on file type
                with st.spinner("Extracting text from file..."):
                    try:
                        if uploaded_file.type == "text/plain":
                            # Handle TXT files
                            input_text = str(uploaded_file.read(), "utf-8")
                            
                        elif uploaded_file.type == "application/pdf":
                            # Handle PDF files
                            pdf_reader = PyPDF2.PdfReader(uploaded_file)
                            text_parts = []
                            for page_num, page in enumerate(pdf_reader.pages):
                                try:
                                    text_parts.append(page.extract_text())
                                except:
                                    st.warning(f"Could not read page {page_num + 1}")
                            input_text = "\n".join(text_parts)
                            
                        elif uploaded_file.type == "text/csv":
                            # Handle CSV files
                            df = pd.read_csv(uploaded_file)
                            input_text = df.to_string()
                            
                        elif uploaded_file.type in ["application/vnd.ms-excel", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"]:
                            # Handle Excel files
                            df = pd.read_excel(uploaded_file)
                            input_text = df.to_string()
                            
                        elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                            # Handle Word documents
                            doc = docx.Document(uploaded_file)
                            text_parts = []
                            for paragraph in doc.paragraphs:
                                text_parts.append(paragraph.text)
                            input_text = "\n".join(text_parts)
                        
                        else:
                            st.error(f"Unsupported file type: {uploaded_file.type}")
                            input_text = ""
                        
                        # Show extraction results
                        if input_text.strip():
                            char_count = len(input_text)
                            st.success(f"✅ Successfully extracted {char_count:,} characters")
                            
                            # Show preview of extracted text
                            if char_count > 500:
                                preview_text = input_text[:500] + "..."
                                st.text_area("Text preview (first 500 characters):", preview_text, height=150, key="preview")
                            else:
                                st.text_area("Extracted text:", input_text, height=150, key="preview")
                            
                            # Warning for very long texts
                            if char_count > 5000:
                                st.warning("⚠️ Text is quite long. Translation may take more time and consume more API credits.")
                            
                            # Update file processing counter (Step 10.4)
                            st.session_state.file_count += 1
                        else:
                            st.error("❌ No text content found in the file")
                            
                    except Exception as e:
                        st.error(f"❌ Error processing file: {str(e)}")
                        input_text = ""

    # Language selection
    target_language = st.selectbox("Select target language:", list(SUPPORTED_LANGUAGES.keys()))
    
    # Translate button with enhanced validation
    if st.button("🔄 Translate", type="primary"):
        # Update translation attempts counter (Step 10.4)
        st.session_state.translation_attempts += 1
        
        # Validate input text
        is_valid, validation_error = validate_text_length(input_text)
        
        if not is_valid:
            st.error(f"❌ {validation_error}")
        else:
            # Show input language detection
            language_info = detect_language_info(input_text)
            st.info(f"🔍 Input text analysis: {language_info}")
            
            with st.spinner(f"Translating to {target_language}..."):
                try:
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    prompt = f"Translate this to {target_language}, return only the translation:\n{input_text}"
                    response = model.generate_content(prompt)
                    
                    # Validate response
                    if response.text and response.text.strip():
                        # Store translation in session state
                        st.session_state.translated_text = response.text.strip()
                        st.session_state.current_language = target_language
                        # Update successful translation counter (Step 10.4)
                        st.session_state.translation_count += 1
                        st.success("✅ Translation completed!")
                    else:
                        st.error("❌ Translation returned empty result. Please try again.")
                                        
                except Exception as e:
                    error_msg = str(e)
                    if "quota" in error_msg.lower():
                        st.error("❌ API quota exceeded. Please check your Gemini API usage limits.")
                    elif "invalid" in error_msg.lower():
                        st.error("❌ Invalid API key. Please check your Gemini API key.")
                    elif "network" in error_msg.lower() or "connection" in error_msg.lower():
                        st.error("❌ Network error. Please check your internet connection and try again.")
                    else:
                        st.error(f"❌ Translation failed: {error_msg}")

    # Show translation result if we have one
    if st.session_state.translated_text:
        st.subheader(f"Translation Result ({st.session_state.current_language}):")
        st.text_area("Translated text:", st.session_state.translated_text, height=100, key="translation_display")

        # TTS SECTION - Persistent outside translation button
        st.subheader("🔊 Text-to-Speech")

        col1, col2 = st.columns(2)

        with col1:
            # Speech speed option
            speech_speed = st.radio("Speech speed:", ["Normal", "Slow"])
            slow_speech = speech_speed == "Slow"

        with col2:
            # Generate audio button with enhanced error handling
            if st.button("🎵 Generate Audio", type="secondary"):
                # Update audio attempts counter (Step 10.4)
                st.session_state.audio_attempts += 1
                
                language_code = SUPPORTED_LANGUAGES[st.session_state.current_language]["code"]
                
                with st.spinner("Generating audio..."):
                    try:
                        # Create TTS object
                        tts = gTTS(text=st.session_state.translated_text, lang=language_code, slow=slow_speech)
                        
                        # Create audio buffer
                        audio_buffer = io.BytesIO()
                        tts.write_to_fp(audio_buffer)
                        audio_buffer.seek(0)
                        
                        # Store in session state
                        st.session_state.audio_data = audio_buffer.getvalue()
                        st.session_state.audio_language = st.session_state.current_language
                        # Update successful audio counter (Step 10.4)
                        st.session_state.audio_count += 1
                        
                        st.success("✅ Audio generated successfully!")
                        
                    except Exception as e:
                        error_msg = str(e)
                        if "language" in error_msg.lower():
                            st.error(f"❌ Language '{st.session_state.current_language}' may not be supported for text-to-speech.")
                        elif "network" in error_msg.lower():
                            st.error("❌ Network error during audio generation. Please try again.")
                        else:
                            st.error(f"❌ Audio generation failed: {error_msg}")

        # Audio playback section - Shows when audio is available
        if st.session_state.audio_data is not None:
            st.subheader("🎧 Audio Playback")
            
            # Play audio
            st.audio(st.session_state.audio_data, format='audio/mp3')
            
            # Download button with sanitized filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            safe_language = sanitize_filename(st.session_state.current_language)
            filename = f"translation_{safe_language}_{timestamp}.mp3"
            
            st.download_button(
                label="⬇️ Download Audio File",
                data=st.session_state.audio_data,
                file_name=filename,
                mime="audio/mp3",
                help="Download the generated audio as MP3 file"
            )

else:
    st.warning("⚠️ Please enter your Gemini API key in the sidebar to get started.")
    
    # Show help for getting API key
    with st.expander("🔑 How to get a Gemini API key"):
        st.markdown("""
        1. Go to [Google AI Studio](https://aistudio.google.com/)
        2. Sign in with your Google account
        3. Click "Get API Key" → "Create API Key"
        4. Copy the generated key (starts with "AIza...")
        5. Paste it in the sidebar above
        
        **Note:** The API key is free to use with generous limits for personal projects.
        """)

# Footer with app info
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 20px;'>
    <p>🌍 Universal Text Translator & Speech Converter</p>
    <p>Built with Streamlit • Powered by Google Gemini API & gTTS</p>
</div>
""", unsafe_allow_html=True)