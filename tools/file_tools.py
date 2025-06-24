import base64
import mimetypes
from pathlib import Path

def encode_file_to_base64(file_content: bytes, filename: str) -> str:
    """Encode file content to base64 with metadata"""
    try:
        encoded = base64.b64encode(file_content).decode('utf-8')
        mime_type = mimetypes.guess_type(filename)[0] or 'application/octet-stream'
        
        return f"File: {filename}\nMIME Type: {mime_type}\nSize: {len(file_content)} bytes\nBase64 Content:\n{encoded}"
    except Exception as e:
        return f"File encoding failed: {str(e)}"

def analyze_file_type(filename: str) -> str:
    """Analyze file type and provide information"""
    try:
        path = Path(filename)
        extension = path.suffix.lower()
        mime_type = mimetypes.guess_type(filename)[0]
        
        file_info = {
            '.pdf': 'PDF Document - Can be processed for text extraction',
            '.txt': 'Plain Text File - Can be read directly',
            '.md': 'Markdown File - Formatted text document',
            '.json': 'JSON Data File - Structured data format',
            '.csv': 'CSV File - Comma-separated values for data analysis',
            '.xlsx': 'Excel Spreadsheet - Can be processed for data extraction',
            '.docx': 'Word Document - Can be processed for text extraction',
            '.jpg': 'JPEG Image - Can be analyzed for content',
            '.png': 'PNG Image - Can be analyzed for content',
            '.py': 'Python Script - Programming code file',
            '.js': 'JavaScript File - Web programming code',
            '.html': 'HTML File - Web page markup',
            '.css': 'CSS File - Web styling code'
        }
        
        description = file_info.get(extension, 'Unknown file type')
        
        return f"File: {filename}\nExtension: {extension}\nMIME Type: {mime_type or 'Unknown'}\nDescription: {description}"
        
    except Exception as e:
        return f"File analysis failed: {str(e)}"