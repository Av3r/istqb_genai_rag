from app.chunker import chunk_text, chunk_text_with_overlap, chunk_text_with_overlap_new
from app.cleaner_pdf import clean_pages
from app.embedder import embed_single
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

    #test embedding single query
    test_embed = embed_single("Which of the following statements BEST describes the relation between multimodal LLMs and vision-language models?")
    print(test_embed)
    
    #chunks = chunk_text_with_overlap_new(full_cleaned_text)

    #create embeddings and ingest to ES
    #ingest_to_es(chunks)
