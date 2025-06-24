import os
import google.generativeai as genai
import logging

logger = logging.getLogger(__name__)

# Configure logging for Google Generative AI (optional, but good for debugging)
# logging.getLogger('google.generativeai').setLevel(logging.DEBUG)


# The API key will be loaded globally by app/main.py before this module is used.
# It's good practice to get it here for clarity, but rely on main.py to load .env
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Initialize the generative model
# This will be configured only if GEMINI_API_KEY is available.
# If not, the raise in get_summary will catch it.
model = None
if GEMINI_API_KEY:
    try:
        genai.configure(api_key=GEMINI_API_KEY)
        model = genai.GenerativeModel('gemini-2.0-flash')
        logger.info("Gemini model configured successfully in summarizer.py.")
    except Exception as e:
        logger.error(f"Failed to configure Gemini API in summarizer.py: {e}", exc_info=True)
else:
    logger.warning("GEMINI_API_KEY is not set. Gemini model will not be configured.")


def get_summary(paper_text: str) -> str:
    """
    Summarizes the provided paper text using the Google Gemini API.

    Args:
        paper_text (str): The full text of the academic paper.

    Returns:
        str: A concise summary of the paper.
    
    Raises:
        ValueError: If GEMINI_API_KEY is not set or model is not configured.
        Exception: For other issues with the Gemini API call.
    """
    global model # Ensure we are using the globally configured model instance

    if not GEMINI_API_KEY or model is None:
        raise ValueError("Gemini API key is not configured or model failed to initialize. Cannot generate summary.")

    # Truncate text if it's too long for the model's context window.
    # Gemini 2.0 Flash has a large context window (1 million tokens),
    # but it's good practice to handle extremely large inputs as a safeguard.
    # 800,000 characters is a generous estimate for 1 million tokens.
    max_model_input_length = 800000 
    if len(paper_text) > max_model_input_length:
        logger.warning(f"Paper text too long ({len(paper_text)} chars), truncating for model input.")
        paper_text = paper_text[:max_model_input_length]

    # Prepare the prompt for summarization
    prompt = f"Please summarize the following academic paper text concisely and clearly. Focus on the main objective, methods, key findings, and conclusions. Maintain a neutral and objective tone.\n\nPaper text:\n{paper_text}"

    logger.info("Sending text to Gemini for summarization...")
    try:
        response = model.generate_content(prompt)
        
        # Access the text content from the response
        if response.candidates and response.candidates[0].content and response.candidates[0].content.parts:
            summary = response.candidates[0].content.parts[0].text
            logger.info("Summary received from Gemini.")
            return summary
        else:
            logger.error(f"Gemini API did not return text content. Full response: {response}")
            return "Could not generate summary: AI model response was empty or malformed."
    except Exception as e:
        logger.error(f"Error calling Gemini API: {e}", exc_info=True)
        # Re-raise the exception or return an error message to be handled by the caller
        raise Exception(f"Failed to get summary from AI model: {e}")

