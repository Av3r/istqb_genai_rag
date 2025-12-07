from app.cleaner_pdf import clean_pages
from app.loader_pdf import load_pdf


patterns_to_remove = [
        r"v\d+\.\d+\s*Page\s*\d+\s*of\s*\d+",   # np. "v1.0 Page 16 of 70"
        r"\d{1,2}\/\d{1,2}\/\d{4}",               # date in format like 25/07/2025
        r"©\s*International\s*Software\s*Testing\s*Qualifications\s*Board",  # copyright
        r"Certified Tester Specialist Level Syllabus –\s*Testing with Generative AI \(CT-GenAI\)",
        r"^Page\s*\d+\s*$",  
    ]

if __name__ == "__main__":
    #load pdf
    pages = load_pdf("syllabus_genai.pdf")
    print(f"\n[INFO] Pages loaded: {len(pages)}")
    #print(pages[15])

    #clean pdf
    clean = clean_pages(pages, patterns_to_remove)

    print(f"\n[INFO] Cleaned pages: {len(clean)}")
    print(clean[0])
