import os


class Settings:
    """Simple settings holder. Loads from environment.

    For production you can replace with pydantic.BaseSettings.
    """

    def __init__(self):
        self.OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
        self.RAG_TOP_K = int(os.getenv("RAG_TOP_K", "5"))
        self.RAG_MIN_SCORE = float(os.getenv("RAG_MIN_SCORE", "1.05"))
        self.OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

        # basic validation
        if not self.OPENAI_API_KEY:
            raise RuntimeError("OPENAI_API_KEY is not set. Provide it via environment or .env file.")


def load_settings() -> Settings:
    return Settings()
