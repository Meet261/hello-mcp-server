import os
import openai
import google.generativeai as genai

def chat_with_openai(message: str, model: str = "gpt-3.5-turbo") -> str:
    """Chat with OpenAI models"""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return "OpenAI API key not configured"
    
    try:
        client = openai.OpenAI(api_key=api_key)
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": message}],
            max_tokens=1000
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"OpenAI chat failed: {str(e)}"

def translate_text(text: str, target_language: str = "Spanish") -> str:
    """Translate text using Gemini"""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return "Gemini API key not configured"
    
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-pro')
        
        prompt = f"Translate the following text to {target_language}. Only return the translation:\n\n{text}"
        response = model.generate_content(prompt)
        
        if response.candidates and response.candidates[0].content:
            return response.candidates[0].content.parts[0].text
        else:
            return "Translation failed"
    except Exception as e:
        return f"Translation error: {str(e)}"

def analyze_sentiment(text: str) -> str:
    """Analyze sentiment of text"""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return "Gemini API key not configured"
    
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-pro')
        
        prompt = f"Analyze the sentiment of this text and provide a brief explanation:\n\n{text}"
        response = model.generate_content(prompt)
        
        if response.candidates and response.candidates[0].content:
            return response.candidates[0].content.parts[0].text
        else:
            return "Sentiment analysis failed"
    except Exception as e:
        return f"Sentiment analysis error: {str(e)}"