
"""
Create the LLM used by the personal assistant.

This file loads environment variables and builds either an OpenAI
or a Gemini chat model, based on LLM_PROVIDER.

Keep it small so beginners can see exactly where the LLM comes from.
"""

import os

from dotenv import load_dotenv


def get_setting(name, default=""):
    """Read Streamlit Cloud Secrets or local environment variables."""
    try:
        import streamlit as st

        if name in st.secrets:
            return str(st.secrets[name])
    except Exception:
        pass

    return os.getenv(name, default)


def get_llm():
    """
    Load settings and create a chat LLM.

    Reads:
        LLM_PROVIDER — "openai" or "gemini" (default: openai)
        OPENAI_API_KEY — required when provider is openai
        OPENAI_MODEL — OpenAI model name (default: gpt-4o-mini)
        GEMINI_API_KEY — required when provider is gemini
        GEMINI_MODEL — Gemini model name (default: gemini-2.5-flash)
    """
    # Load variables from a local .env file (if present).
    load_dotenv()

    provider = get_setting("LLM_PROVIDER", "openai").strip().lower()

    if provider == "openai":
        return _create_openai_llm()

    if provider == "gemini":
        return _create_gemini_llm()

    raise ValueError(
        f'Unknown LLM_PROVIDER: "{provider}". '
        'Use "openai" or "gemini" in your configuration.'
    )


def _create_openai_llm():
    """Create a ChatOpenAI client."""
    from langchain_openai import ChatOpenAI

    api_key = get_setting("OPENAI_API_KEY").strip()
    if not api_key:
        raise ValueError(
            "OPENAI_API_KEY is missing. "
            "Add it to your .env file or Streamlit Secrets."
        )

    model = get_setting("OPENAI_MODEL", "gpt-4o-mini").strip()

    llm = ChatOpenAI(
        model=model,
        api_key=api_key,
        temperature=0,
    )
    return llm


def _create_gemini_llm():
    """Create a Gemini chat model."""
    from langchain_google_genai import ChatGoogleGenerativeAI

    api_key = get_setting("GEMINI_API_KEY").strip()
    if not api_key:
        raise ValueError(
            "GEMINI_API_KEY is missing. "
            "Add it to your .env file or Streamlit Secrets."
        )

    model = get_setting("GEMINI_MODEL", "gemini-2.5-flash").strip()

    llm = ChatGoogleGenerativeAI(
        model=model,
        google_api_key=api_key,
        temperature=0,
    )
    return llm
