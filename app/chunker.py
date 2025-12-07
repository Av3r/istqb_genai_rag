def chunk_text(texts, max_chars=1500):
    chunks = []
    current = ""

    for txt in texts:
        for line in txt.split("\n"):
            if len(current) + len(line) > max_chars:
                chunks.append(current)
                current = line
            else:
                current += "\n" + line

    if current.strip():
        chunks.append(current)

    return chunks