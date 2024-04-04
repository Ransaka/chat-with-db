import re

pattern = r'\b[\w-]+\.csv\b'

def get_file_names(text):
    matches = re.findall(pattern, text)
    if matches:
        return matches[0]
    else:
        return text
