from typing import Union

def validate_input(text: str) -> bool:
    """Validate user input for skill/role"""
    return len(text.strip()) > 2 and any(c.isalpha() for c in text)

def format_content(text: str) -> str:
    """Format generated content for better display"""
    if not text:
        return ""
    
    # Convert markdown lists to streamlit format
    text = text.replace('- ', '• ')
    
    # Bold section headers
    lines = []
    for line in text.split('\n'):
        if line.strip().endswith(':'):
            line = f"**{line}**"
        lines.append(line)
    
    return '\n'.join(lines)

def handle_errors(func):
    """Decorator for error handling"""
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            return f"Error in {func.__name__}: {str(e)}"
    return wrapper