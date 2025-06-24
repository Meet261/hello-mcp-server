import json
import csv
from io import StringIO
import re

def parse_json(json_string: str) -> str:
    """Parse and format JSON data"""
    try:
        data = json.loads(json_string)
        formatted = json.dumps(data, indent=2, ensure_ascii=False)
        return f"Parsed JSON:\n```json\n{formatted}\n```"
    except json.JSONDecodeError as e:
        return f"Invalid JSON: {str(e)}"

def parse_csv(csv_string: str, delimiter: str = ",") -> str:
    """Parse CSV data and return formatted table"""
    try:
        csv_file = StringIO(csv_string)
        reader = csv.reader(csv_file, delimiter=delimiter)
        rows = list(reader)
        
        if not rows:
            return "Empty CSV data"
        
        # Format as table
        result = "CSV Data:\n"
        for i, row in enumerate(rows[:10]):  # Limit to first 10 rows
            if i == 0:
                result += "| " + " | ".join(row) + " |\n"
                result += "|" + "|".join(["-" * (len(cell) + 2) for cell in row]) + "|\n"
            else:
                result += "| " + " | ".join(row) + " |\n"
        
        if len(rows) > 10:
            result += f"\n... and {len(rows) - 10} more rows"
        
        return result
    except Exception as e:
        return f"CSV parsing failed: {str(e)}"

def extract_emails(text: str) -> str:
    """Extract email addresses from text"""
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    emails = re.findall(email_pattern, text)
    
    if emails:
        unique_emails = list(set(emails))
        return f"Found {len(unique_emails)} unique email addresses:\n" + "\n".join(f"• {email}" for email in unique_emails)
    else:
        return "No email addresses found in the text"

def extract_urls(text: str) -> str:
    """Extract URLs from text"""
    url_pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
    urls = re.findall(url_pattern, text)
    
    if urls:
        unique_urls = list(set(urls))
        return f"Found {len(unique_urls)} unique URLs:\n" + "\n".join(f"• {url}" for url in unique_urls)
    else:
        return "No URLs found in the text"