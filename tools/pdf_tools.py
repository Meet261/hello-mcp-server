import os
import google.generativeai as genai
from utils.helpers import download_pdf, extract_text
from utils.validators import validate_url, validate_text_length, validate_api_key_format

def summarize_pdf_from_url(url: str) -> str:
    """Download PDF from URL and summarize it"""
    # Validate URL
    is_valid, error_msg = validate_url(url)
    if not is_valid:
        return f"Invalid URL: {error_msg}"
    
    try:
        pdf_content = download_pdf(url)
        text = extract_text(pdf_content)
        return summarize_text(text)
    except Exception as e:
        return f"Error processing PDF: {str(e)}"

def summarize_text(text: str) -> str:
    """Summarize provided text using Gemini"""
    # Validate text length
    is_valid, error_msg = validate_text_length(text, min_length=10, max_length=100000)
    if not is_valid:
        return f"Text validation failed: {error_msg}"
    
    # Validate API key
    api_key = os.getenv("GEMINI_API_KEY")
    is_valid, error_msg = validate_api_key_format(api_key, "gemini")
    if not is_valid:
        return f"API key validation failed: {error_msg}"
    
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.0-flash')
        
        prompt = f"Summarize this text concisely:\n\n{text}"
        response = model.generate_content(prompt)
        
        if response.candidates and response.candidates[0].content:
            return response.candidates[0].content.parts[0].text
        else:
            return "Failed to generate summary"
    except Exception as e:
        return f"Summarization error: {str(e)}"