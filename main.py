from app.chunker import chunk_text, chunk_text_with_overlap, chunk_text_with_overlap_new
from app.cleaner_pdf import clean_pages
from app.ingest import ingest_to_es
from app.loader_pdf import load_pdf


patterns_to_remove = [
        r"v\d+\.\d+\s*Page\s*\d+\s*of\s*\d+",   # np. "v1.0 Page 16 of 70"
        r"\d{1,2}\/\d{1,2}\/\d{4}",               # date in format like 25/07/2025
        r"©\s*International\s*Software\s*Testing\s*Qualifications\s*Board",  # copyright
        r"Certified Tester Specialist Level Syllabus –\s*Testing with Generative AI \(CT-GenAI\)",
        r"^Page\s*\d+\s*$",
        r"^[•o]\s*",  # bullet points (• and o) at start of line
    ]
  

if __name__ == "__main__":
    #load pdf
    pages = load_pdf("syllabus_genai.pdf")
    #print(f"\n[INFO] Pages loaded: {len(pages)}")
    #print(pages[15])

    #clean pdf
    cleaned = clean_pages(pages, patterns_to_remove)

    #join all cleaned pages into one continuous text
    full_cleaned_text = "\n".join(cleaned)

    #print(full_cleaned_text)
    
    chunks = chunk_text_with_overlap_new(full_cleaned_text)

    print(f'[INFO] tests chunk: {chunks[0]}')
    print(f'[INFO] tests chunk: {chunks[1]}')
    print(f'[INFO] tests chunk: {chunks[2]}')
    print(f'[INFO] tests chunk: {chunks[3]}')
    print(f'[INFO] tests chunk: {chunks[4]}')
    print(f'[INFO] tests chunk: {chunks[5]}')
    print(f'[INFO] tests chunk: {chunks[6]}')

    #ingest_to_es(chunks)
    

    #print(f"\n[INFO] Cleaned pages: {len(cleaned)}")
    #print(cleaned[0])
