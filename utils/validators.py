import re
import urllib.parse
from typing import Optional, List, Dict, Any
import json

def validate_url(url: str) -> tuple[bool, str]:
    """
    Validate if a string is a proper URL
    Returns: (is_valid, error_message)
    """
    if not url or not isinstance(url, str):
        return False, "URL cannot be empty"
    
    try:
        result = urllib.parse.urlparse(url)
        if not all([result.scheme, result.netloc]):
            return False, "URL must include scheme (http/https) and domain"
        
        if result.scheme not in ['http', 'https']:
            return False, "URL must use http or https protocol"
        
        return True, ""
    except Exception as e:
        return False, f"Invalid URL format: {str(e)}"

def validate_email(email: str) -> tuple[bool, str]:
    """
    Validate email address format
    Returns: (is_valid, error_message)
    """
    if not email or not isinstance(email, str):
        return False, "Email cannot be empty"
    
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    if re.match(email_pattern, email):
        return True, ""
    else:
        return False, "Invalid email format"

def validate_json(json_string: str) -> tuple[bool, str, Optional[Dict]]:
    """
    Validate JSON string
    Returns: (is_valid, error_message, parsed_data)
    """
    if not json_string or not isinstance(json_string, str):
        return False, "JSON string cannot be empty", None
    
    try:
        parsed = json.loads(json_string)
        return True, "", parsed
    except json.JSONDecodeError as e:
        return False, f"Invalid JSON: {str(e)}", None

def validate_text_length(text: str, min_length: int = 1, max_length: int = 100000) -> tuple[bool, str]:
    """
    Validate text length constraints
    Returns: (is_valid, error_message)
    """
    if not isinstance(text, str):
        return False, "Input must be a string"
    
    if len(text) < min_length:
        return False, f"Text must be at least {min_length} characters long"
    
    if len(text) > max_length:
        return False, f"Text must be no more than {max_length} characters long"
    
    return True, ""

def validate_language_code(language: str) -> tuple[bool, str]:
    """
    Validate language code/name for translation
    Returns: (is_valid, error_message)
    """
    if not language or not isinstance(language, str):
        return False, "Language cannot be empty"
    
    # Common language codes and names
    valid_languages = {
        # Language codes
        'en', 'es', 'fr', 'de', 'it', 'pt', 'ru', 'ja', 'ko', 'zh', 'ar', 'hi',
        'nl', 'sv', 'da', 'no', 'fi', 'pl', 'tr', 'he', 'th', 'vi', 'id', 'ms',
        
        # Language names (common ones)
        'english', 'spanish', 'french', 'german', 'italian', 'portuguese', 
        'russian', 'japanese', 'korean', 'chinese', 'arabic', 'hindi',
        'dutch', 'swedish', 'danish', 'norwegian', 'finnish', 'polish',
        'turkish', 'hebrew', 'thai', 'vietnamese', 'indonesian', 'malay'
    }
    
    if language.lower() in valid_languages:
        return True, ""
    else:
        return False, f"Unsupported language: {language}. Please use common language names or ISO codes."

def validate_file_extension(filename: str, allowed_extensions: List[str]) -> tuple[bool, str]:
    """
    Validate file extension
    Returns: (is_valid, error_message)
    """
    if not filename or not isinstance(filename, str):
        return False, "Filename cannot be empty"
    
    if '.' not in filename:
        return False, "Filename must have an extension"
    
    extension = filename.lower().split('.')[-1]
    allowed_extensions = [ext.lower().lstrip('.') for ext in allowed_extensions]
    
    if extension in allowed_extensions:
        return True, ""
    else:
        return False, f"File extension '.{extension}' not allowed. Allowed: {', '.join(['.' + ext for ext in allowed_extensions])}"

def validate_csv_delimiter(delimiter: str) -> tuple[bool, str]:
    """
    Validate CSV delimiter
    Returns: (is_valid, error_message)
    """
    if not delimiter or not isinstance(delimiter, str):
        return False, "Delimiter cannot be empty"
    
    if len(delimiter) != 1:
        return False, "Delimiter must be a single character"
    
    valid_delimiters = [',', ';', '\t', '|', ':']
    if delimiter in valid_delimiters:
        return True, ""
    else:
        return False, f"Invalid delimiter '{delimiter}'. Common delimiters: {', '.join(valid_delimiters)}"

def validate_number_range(value: Any, min_val: float = None, max_val: float = None) -> tuple[bool, str]:
    """
    Validate number is within range
    Returns: (is_valid, error_message)
    """
    try:
        num_value = float(value)
    except (ValueError, TypeError):
        return False, f"'{value}' is not a valid number"
    
    if min_val is not None and num_value < min_val:
        return False, f"Value {num_value} is below minimum {min_val}"
    
    if max_val is not None and num_value > max_val:
        return False, f"Value {num_value} is above maximum {max_val}"
    
    return True, ""

def validate_openai_model(model: str) -> tuple[bool, str]:
    """
    Validate OpenAI model name
    Returns: (is_valid, error_message)
    """
    if not model or not isinstance(model, str):
        return False, "Model name cannot be empty"
    
    valid_models = [
        'gpt-4', 'gpt-4-turbo', 'gpt-4-turbo-preview',
        'gpt-3.5-turbo', 'gpt-3.5-turbo-16k',
        'text-davinci-003', 'text-davinci-002',
        'code-davinci-002'
    ]
    
    if model in valid_models:
        return True, ""
    else:
        return False, f"Unsupported model '{model}'. Supported models: {', '.join(valid_models)}"

def sanitize_filename(filename: str) -> str:
    """
    Sanitize filename by removing/replacing invalid characters
    """
    if not filename:
        return "untitled"
    
    # Remove or replace invalid characters
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, '_')
    
    # Remove leading/trailing spaces and dots
    filename = filename.strip(' .')
    
    # Ensure it's not empty after sanitization
    if not filename:
        return "untitled"
    
    return filename

def validate_api_key_format(api_key: str, key_type: str = "generic") -> tuple[bool, str]:
    """
    Validate API key format based on type
    Returns: (is_valid, error_message)
    """
    if not api_key or not isinstance(api_key, str):
        return False, f"{key_type} API key cannot be empty"
    
    api_key = api_key.strip()
    
    if key_type.lower() == "openai":
        if not api_key.startswith("sk-"):
            return False, "OpenAI API key must start with 'sk-'"
        if len(api_key) < 20:
            return False, "OpenAI API key appears too short"
    
    elif key_type.lower() == "gemini":
        if len(api_key) < 20:
            return False, "Gemini API key appears too short"
    
    elif key_type.lower() == "weather":
        if len(api_key) < 10:
            return False, "Weather API key appears too short"
    
    return True, ""

def validate_coordinates(lat: float, lon: float) -> tuple[bool, str]:
    """
    Validate latitude and longitude coordinates
    Returns: (is_valid, error_message)
    """
    try:
        lat = float(lat)
        lon = float(lon)
    except (ValueError, TypeError):
        return False, "Coordinates must be valid numbers"
    
    if not (-90 <= lat <= 90):
        return False, f"Latitude {lat} must be between -90 and 90"
    
    if not (-180 <= lon <= 180):
        return False, f"Longitude {lon} must be between -180 and 180"
    
    return True, ""

# Validation decorator for tool functions
def validate_inputs(**validators):
    """
    Decorator to validate function inputs
    Usage: @validate_inputs(url=validate_url, text=validate_text_length)
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            # Get function parameter names
            import inspect
            sig = inspect.signature(func)
            param_names = list(sig.parameters.keys())
            
            # Map positional args to parameter names
            bound_args = sig.bind(*args, **kwargs)
            bound_args.apply_defaults()
            
            # Validate each specified parameter
            for param_name, validator in validators.items():
                if param_name in bound_args.arguments:
                    value = bound_args.arguments[param_name]
                    
                    if callable(validator):
                        is_valid, error_msg = validator(value)
                        if not is_valid:
                            raise ValueError(f"Validation failed for {param_name}: {error_msg}")
            
            return func(*args, **kwargs)
        return wrapper
    return decorator