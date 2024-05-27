import re

def detect_language(query):
    supported_languages = [
        "python", "javascript", "java", "csharp", "c#", "c", "cpp", "html", "css", "react"
    ]
    
    pattern = re.compile(r'\b(' + '|'.join(supported_languages) + r')\b', re.IGNORECASE)
    
    match = pattern.search(query)
    
    if match:
        return match.group(0).lower()
    else:
        return None


print(detect_language("I need a recursion function python"))