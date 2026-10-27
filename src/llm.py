"""
Create the LLM used by the personal assistant.

This file loads environment variables and builds either an OpenAI
or a Gemini chat model, based on LLM_PROVIDER in the .env file.

Keep it small so beginners can see exactly where the LLM comes from.
"""

import os

from dotenv import load_dotenv


def get_llm():
    """
    Load settings from .env and create a chat LLM.

    Reads:
        LLM_PROVIDER — "openai" or "gemini" (default: openai)
        OPENAI_API_KEY — required when provider is openai
        OPENAI_MODEL — OpenAI model name (default: gpt-4o-mini)
        GEMINI_API_KEY — required when provider is gemini
        GEMINI_MODEL — Gemini model name (default: gemini-2.0-flash)

    Returns:
        A chat model ready for tool calling (ChatOpenAI or ChatGoogleGenerativeAI).

    Example:
        llm = get_llm()
        reply = llm.invoke("Hello!")
        print(reply.content)
    """
    # Load variables from a local .env file (if present).
    load_dotenv()

    provider = os.getenv("LLM_PROVIDER", "openai").strip().lower()

    # temperature=0 keeps answers more consistent for demos/lectures.
    if provider == "openai":
        return _create_openai_llm()

    if provider == "gemini":
        return _create_gemini_llm()

    raise ValueError(
        f'Unknown LLM_PROVIDER: "{provider}". '
        'Use "openai" or "gemini" in your .env file.'
    )


def _create_openai_llm():
    """
    Create a ChatOpenAI client using the OpenAI API key from .env.

    Returns:
        ChatOpenAI: An OpenAI chat model instance.

    Raises:
        ValueError: If OPENAI_API_KEY is missing.
    """
    from langchain_openai import ChatOpenAI

    api_key = os.getenv("OPENAI_API_KEY", "").strip()
    if not api_key:
        raise ValueError(
            "OPENAI_API_KEY is missing. "
            "Add it to your .env file when LLM_PROVIDER=openai."
        )

    model = os.getenv("OPENAI_MODEL", "gpt-4o-mini").strip()

    llm = ChatOpenAI(
        model=model,
        api_key=api_key,
        temperature=0,
    )
    return llm


def _create_gemini_llm():
    """
    Create a ChatGoogleGenerativeAI client using the Gemini API key from .env.

    Returns:
        ChatGoogleGenerativeAI: A Gemini chat model instance.

    Raises:
        ValueError: If GEMINI_API_KEY is missing.
    """
    from langchain_google_genai import ChatGoogleGenerativeAI

    api_key = os.getenv("GEMINI_API_KEY", "").strip()
    if not api_key:
        raise ValueError(
            "GEMINI_API_KEY is missing. "
            "Add it to your .env file when LLM_PROVIDER=gemini."
        )

    model = os.getenv("GEMINI_MODEL", "gemini-2.0-flash").strip()

    llm = ChatGoogleGenerativeAI(
        model=model,
        google_api_key=api_key,
        temperature=0,
    )
    return llm