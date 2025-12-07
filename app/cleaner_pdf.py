import re

def clean_pages(pages, patterns_to_remove=None):

    if patterns_to_remove is None:
        patterns_to_remove = []

    cleaned = []
    for p in pages:
        txt = p
        for pattern in patterns_to_remove:
            #txt = re.sub(pattern, "", txt)
            txt = re.sub(pattern, "", txt, flags=re.IGNORECASE | re.MULTILINE)
        cleaned.append(txt.strip())
    return cleaned