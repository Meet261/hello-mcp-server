import os
import google.generativeai as genai
import logging

logger = logging.getLogger(__name__)

# Don't initialize anything globally - do it lazily
_model = None
_initialized = False

def _ensure_initialized():
    """Initialize Gemini API only when needed."""
    global _model, _initialized
    
    if _initialized:
        return _model
    
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    
    if not GEMINI_API_KEY:
        raise ValueError("GEMINI_API_KEY environment variable is not set")
    
    try:
        genai.configure(api_key=GEMINI_API_KEY)
        _model = genai.GenerativeModel('gemini-2.0-flash')
        _initialized = True
        logger.info("Gemini model configured successfully.")
        return _model
    except Exception as e:
        logger.error(f"Failed to configure Gemini API: {e}", exc_info=True)
        raise ValueError(f"Failed to initialize Gemini API: {e}")

def get_summary(paper_text: str) -> str:
    """
    Summarizes the provided paper text using the Google Gemini API.
    """
    # Initialize only when actually called
    model = _ensure_initialized()

    max_model_input_length = 800000 
    if len(paper_text) > max_model_input_length:
        logger.warning(f"Paper text too long ({len(paper_text)} chars), truncating.")
        paper_text = paper_text[:max_model_input_length]

    prompt = f"Please summarize the following academic paper text concisely and clearly. Focus on the main objective, methods, key findings, and conclusions.\n\nPaper text:\n{paper_text}"

    logger.info("Sending text to Gemini for summarization...")
    try:
        response = model.generate_content(prompt)
        
        if response.candidates and response.candidates[0].content and response.candidates[0].content.parts:
            summary = response.candidates[0].content.parts[0].text
            logger.info("Summary received from Gemini.")
            return summary
        else:
            logger.error(f"Gemini API returned empty response: {response}")
            return "Could not generate summary: AI model response was empty."
    except Exception as e:
        logger.error(f"Error calling Gemini API: {e}", exc_info=True)
        raise Exception(f"Failed to get summary from AI model: {e}")