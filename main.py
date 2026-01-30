from dotenv import load_dotenv
load_dotenv()

import os
from openai import OpenAI

from app.config import load_settings
from app.rag import RAGService
from app.chunker import chunk_text, chunk_text_with_overlap, chunk_text_with_overlap_new
from app.cleaner_pdf import clean_pages
from app.embedder import embed_single
from app.ingest import ingest_to_es
from app.loader_pdf import load_pdf
from app.verify_top import verify_top_k

patterns_to_remove = [
        r"v\d+\.\d+\s*Page\s*\d+\s*of\s*\d+",   # np. "v1.0 Page 16 of 70"
        r"\d{1,2}\/\d{1,2}\/\d{4}",               # date in format like 25/07/2025
        r"©\s*International\s*Software\s*Testing\s*Qualifications\s*Board",  # copyright
        r"Certified Tester Specialist Level Syllabus –\s*Testing with Generative AI \(CT-GenAI\)",
        r"^Page\s*\d+\s*$",
        r"^[•o]\s*",  # bullet points (• and o) at start of line
    ]
  
def run_ingest():
    pages = load_pdf("syllabus_genai.pdf")
    cleaned = clean_pages(pages, patterns_to_remove)
    full_cleaned_text = "\n".join(cleaned)
    chunks = chunk_text_with_overlap_new(full_cleaned_text)
    ingest_to_es(chunks)


if __name__ == "__main__":
    settings = load_settings()

    # create OpenAI client and RAG service (dependency injection)
    client = OpenAI(api_key=settings.OPENAI_API_KEY)
    rag_service = RAGService(client, settings)

    # inspect top-k retrieval
    veryfy = verify_top_k("test czy po polsku cos ogarnie?", k=settings.RAG_TOP_K)
    print(veryfy)
    print("\n\n=== RAG ANSWER ===")

    rag_response = rag_service.answer(
        """Which of the following statements BEST explains the difference between AI chatbots and LLMpowered
testing applications in the context of software testing?
a) AI chatbots are more suited for specific test tasks, while LLM-powered testing applications
focus on ad hoc interactions.
b) Both AI chatbots and LLM-powered testing applications are designed to perform identical
tasks without any configuration differences.
c) LLM-powered testing applications rely on conversational prompts, while AI chatbots require
integration into test tools and test processes.
d) AI chatbots offer conversational interfaces for ad hoc test tasks, while LLM-powered testing
applications provide customized solutions for specific test tasks.
Select ONE option."""
    )

    print(rag_response)



#     """A tester is examining a structured prompt used to obtain LLM assistance for performance test
# analysis. One of the components of this prompt reads: “Test reports from performance testing tools,
# system monitoring logs during peak usage periods, and application performance benchmarks from
# previous releases”.
# In which component of the six-part prompt structure would this description MOST LIKELY appear?
# a) Context
# b) Input data
# c) Constraints
# d) Output format
# Select ONE option."""  ##odp B


    # #load pdf
    # pages = load_pdf("syllabus_genai.pdf")
    # #print(f"\n[INFO] Pages loaded: {len(pages)}")
    # #print(pages[15])

    # #clean pdf
    # cleaned = clean_pages(pages, patterns_to_remove)

    # #join all cleaned pages into one continuous text
    # full_cleaned_text = "\n".join(cleaned)


    # #test embedding single query
    # #test_embed = embed_single("Which of the following statements BEST describes the relation between multimodal LLMs and vision-language models?")
    # #print(test_embed)
    
    # chunks = chunk_text_with_overlap_new(full_cleaned_text)

    # print(f'[info] total chunks: {len(chunks)}')
    # # print(f'[info] chunk {chunks[0]}')
    # # print(f'[info] chunk {chunks[1]}')

    # #create embeddings and ingest to ES
    # ingest_to_es(chunks)
