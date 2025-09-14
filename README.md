# Universal Text Translator & Speech Converter
## Generative AI and ML Capstone Project

**Student:** Kyle D Dahgon  
**Course:** Generative AI and ML  
**Institution:** Illinois Tech  
**Date:** 09/14/2025

---

## Project Overview

This capstone project is a comprehensive web application that enables users to translate text into various languages and convert the translated text into speech with downloadable audio files. The application leverages Google's Gemini API for translation and Google Text-to-Speech (gTTS) for speech synthesis, all wrapped in an intuitive Streamlit web interface.

### Key Features
- 🌍 **Multi-language Translation**: Support for 15+ languages using Google Gemini API
- 🔊 **Text-to-Speech**: Convert translations to audio with normal/slow speed options
- 📁 **File Upload Support**: Process TXT, PDF, CSV, Excel, and Word documents
- 🎵 **Audio Download**: Generate and download MP3 files
- 📊 **Usage Statistics**: Track translation and audio generation metrics
- 🔍 **Language Detection**: Automatic detection of input text characteristics
- ⚡ **Real-time Processing**: Instant translation and audio generation
- 🛡️ **Input Validation**: Comprehensive error handling and user feedback

---

## Setup Instructions

### Prerequisites
- Python 3.8 or higher
- Internet connection (required for API calls)
- Google Gemini API key

### 1. Environment Setup

**Create and activate virtual environment:**
```bash
# Create project directory
mkdir translation-app
cd translation-app

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate

# You should see (venv) in your terminal prompt
```

### 2. Install Dependencies

```bash
# Install required packages
pip install streamlit
pip install google-generativeai
pip install gtts
pip install PyPDF2
pip install openpyxl
pip install python-docx
pip install pandas

# Save requirements for future use
pip freeze > requirements.txt
```

**Alternative installation from requirements.txt:**
```bash
pip install -r requirements.txt
```

### 3. Obtain Google Gemini API Key

**Step-by-step API key setup:**

1. **Visit Google AI Studio:**
   - Go to [https://aistudio.google.com/](https://aistudio.google.com/)
   - Sign in with your Google account

2. **Create API Key:**
   - Click "Get API Key" in the top navigation
   - Select "Create API key in new project" (recommended)
   - Copy the generated API key (starts with "AIzaSy...")
   - **Important:** Store this key securely - it won't be shown again

3. **API Key Security:**
   - Never commit API keys to version control
   - Keep your API key private and secure
   - The key provides access to Google's services under your account

### 4. Run the Application

```bash
# Start the Streamlit application
streamlit run app.py
```

**Expected output:**
```
You can now view your Streamlit app in your browser.

Local URL: http://localhost:8501
Network URL: http://192.168.x.x:8501
```

The application will automatically open in your default web browser at `http://localhost:8501`.

---

## Usage Guide

### Basic Usage Workflow

1. **Configure API Key:**
   - Enter your Gemini API key in the sidebar
   - Wait for "✅ API Key configured!" confirmation

2. **Choose Input Method:**
   - **Type text directly**: Use the text area for manual input
   - **Upload a file**: Support for TXT, PDF, CSV, Excel, Word files

3. **Select Target Language:**
   - Choose from 15+ supported languages
   - Languages include: Spanish, French, German, Italian, Portuguese, Russian, Japanese, Korean, Chinese, Arabic, Hindi, Dutch, Polish, Turkish, Swedish

4. **Translate Text:**
   - Click "🔄 Translate" button
   - View translation results with language detection info

5. **Generate Audio (Optional):**
   - Select speech speed (Normal/Slow)
   - Click "🎵 Generate Audio"
   - Play audio in browser or download MP3 file

### File Upload Guide

**Supported file types and expected behavior:**

- **TXT Files**: Direct text extraction, maintains formatting
- **PDF Files**: Extracts text from all pages, works best with text-based PDFs
- **CSV Files**: Displays data in readable format, processes all columns
- **Excel Files**: Extracts data from active sheet, handles both .xlsx and .xls
- **Word Documents**: Extracts paragraph text, removes formatting

**File limitations:**
- Maximum file size: 10MB
- Maximum text length: 5,000 characters per translation
- Files should not be password-protected

### Advanced Features

**Session Statistics:**
- Track translations, audio generations, and file uploads
- View success rates and session duration
- Reset statistics anytime

**Language Detection:**
- Automatic detection of input text characteristics
- Identifies Chinese, Japanese, Korean, Arabic, Cyrillic, and Latin scripts
- Helps optimize translation quality

**Error Handling:**
- Comprehensive input validation
- Clear error messages for common issues
- Graceful handling of API failures

---

## Technical Implementation

### Architecture Overview

**Frontend:** Streamlit web framework provides the user interface
**Translation Engine:** Google Gemini API for multilingual text translation
**Text-to-Speech:** Google Text-to-Speech (gTTS) for audio generation
**File Processing:** Multiple libraries for different file format support

### Key Components

1. **Translation Module**
   - Google Gemini API integration
   - Error handling and retry logic
   - Response validation

2. **Text-to-Speech Engine**
   - gTTS integration for audio generation
   - Speed control (normal/slow)
   - MP3 file generation and download

3. **File Processing System**
   - Multi-format file support
   - Text extraction and preprocessing
   - File validation and error handling

4. **User Interface**
   - Streamlit-based responsive design
   - Session state management
   - Real-time feedback and statistics

### Dependencies

| Package | Purpose | Version |
|---------|---------|---------|
| streamlit | Web application framework | 1.28.0+ |
| google-generativeai | Google Gemini API client | 0.3.0+ |
| gtts | Google Text-to-Speech | 2.3.2+ |
| PyPDF2 | PDF text extraction | 3.0.1+ |
| openpyxl | Excel file processing | 3.1.2+ |
| python-docx | Word document processing | 0.8.11+ |
| pandas | Data manipulation | 2.0.3+ |

---

## Considerations and Limitations

### API Considerations

**Google Gemini API:**
- **Rate Limits**: Free tier has usage quotas (generous for personal projects)
- **Cost**: Pay-per-use after free quota exhausted
- **Availability**: Requires stable internet connection
- **Quality**: Translation quality varies by language pair and content type

**Google Text-to-Speech:**
- **Language Support**: Limited voice options for some languages
- **Audio Quality**: Synthetic voice quality varies by language
- **Processing Time**: Longer texts take more time to generate audio

### Technical Limitations

**File Processing:**
- **PDF Extraction**: Works best with text-based PDFs; image-based PDFs may have poor extraction
- **File Size**: 10MB limit to prevent performance issues
- **Text Length**: 5,000 character limit per translation to manage API costs
- **Format Support**: Limited to common office document formats

**Performance:**
- **Translation Speed**: Depends on text length and API response time (typically 3-15 seconds)
- **Audio Generation**: Varies by text length (typically 3-10 seconds)
- **Browser Compatibility**: Requires modern browser with JavaScript enabled

### Usage Limitations

**Internet Dependency:**
- Requires active internet connection for all API calls
- No offline translation capability
- Network issues affect functionality

**Language Limitations:**
- Translation quality varies significantly between language pairs
- Some languages have limited TTS voice quality
- Cultural context and idioms may not translate accurately

---

## Challenges Faced During Development

### 1. API Integration Challenges

**Google Gemini API Model Changes:**
- **Issue**: Initial model name `gemini-pro` became deprecated during development
- **Solution**: Implemented dynamic model discovery to find available models
- **Resolution**: Updated to use `gemini-1.5-flash` for optimal performance

**API Key Management:**
- **Issue**: Secure handling of API keys in web application
- **Solution**: Implemented client-side key entry with validation
- **Best Practice**: Added warnings about key security and never storing keys in code

### 2. Streamlit State Management

**Button Interaction Issues:**
- **Issue**: TTS controls disappearing after page refresh due to Streamlit's execution model
- **Solution**: Implemented comprehensive session state management
- **Result**: Persistent UI elements and smooth user experience

**File Upload State:**
- **Issue**: Uploaded files not persisting between interactions
- **Solution**: Proper session state handling for file content and metadata
- **Improvement**: Added file processing counters and statistics

### 3. Text-to-Speech Implementation

**Audio Generation Reliability:**
- **Issue**: Inconsistent audio generation across different languages
- **Solution**: Added comprehensive error handling for TTS failures
- **Enhancement**: Implemented language-specific error messages

**Audio File Management:**
- **Issue**: Browser compatibility for audio playback and download
- **Solution**: Used standard MP3 format with proper MIME types
- **Feature**: Added timestamp-based filename generation

### 4. File Processing Complexity

**Multi-format Support:**
- **Issue**: Different libraries required for various file formats
- **Solution**: Implemented modular file processing with format detection
- **Challenge**: Handling edge cases like corrupted or password-protected files

**Text Extraction Quality:**
- **Issue**: Inconsistent text extraction quality from PDF files
- **Solution**: Added page-by-page processing with error handling
- **Limitation**: Image-based PDFs still have limited extraction capability

### 5. User Experience Optimization

**Input Validation:**
- **Issue**: Users attempting invalid operations (empty input, oversized files)
- **Solution**: Comprehensive input validation with clear error messages
- **Enhancement**: Added real-time character counting and warnings

**Performance Feedback:**
- **Issue**: Users uncertain about processing status during API calls
- **Solution**: Implemented loading spinners and progress indicators
- **Improvement**: Added estimated processing times and tips

### 6. Development Environment

**Dependency Management:**
- **Issue**: Large number of dependencies for file processing
- **Solution**: Created minimal version option with reduced dependencies
- **Learning**: Importance of virtual environments for clean development

**Cross-platform Compatibility:**
- **Issue**: Different Python installation patterns across operating systems
- **Solution**: Provided multiple installation command options
- **Documentation**: Comprehensive setup instructions for various platforms

---

## Future Enhancements

### Potential Improvements

1. **Enhanced Translation Features:**
   - Batch translation for multiple files
   - Translation confidence scores
   - Alternative translation suggestions

2. **Advanced TTS Options:**
   - Multiple voice selections per language
   - Voice emotion and tone controls
   - Audio speed fine-tuning

3. **User Experience:**
   - Translation history and favorites
   - User accounts and saved preferences
   - Dark mode interface option

4. **Technical Enhancements:**
   - Caching for repeated translations
   - Offline mode for basic functionality
   - API usage analytics and cost tracking

---

## Conclusion

This capstone project successfully demonstrates the integration of modern AI services (Google Gemini for translation and gTTS for speech synthesis) into a user-friendly web application. The project showcases proficiency in:

- **API Integration**: Successful integration with Google's AI services
- **Web Development**: Creating responsive, interactive web applications with Streamlit
- **File Processing**: Handling multiple file formats and text extraction
- **Error Handling**: Comprehensive validation and user feedback systems
- **User Experience Design**: Intuitive interface with advanced features

The application provides practical value for breaking down language barriers and making content accessible across different languages and formats. Despite some limitations inherent to AI translation services, the application demonstrates robust functionality suitable for real-world use cases.

**The project fulfills all capstone requirements while providing a foundation for future enhancements and commercial applications.**

---

## Contact Information

**Student:** Kyle D Dahgon  
**Course:** Generative AI and ML Capstone Project  
**Institution:** Illinois Institute of Technology

**Project Repository:** https://github.com/KyleDGorilla/translation-tts-capstone-kd  
**Submission Date:** 09/14/2025
