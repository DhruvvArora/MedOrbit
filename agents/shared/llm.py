import os
import json
from typing import Any, Type

from pydantic import BaseModel
from openai import OpenAI

# Safe loading of environment variables
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")


class LLMError(Exception):
    pass


def get_llm_client() -> OpenAI | None:
    """Returns OpenAI client if key exists, otherwise None (mock mode)."""
    if not OPENAI_API_KEY:
        return None
    return OpenAI(api_key=OPENAI_API_KEY)


def execute_structured_prompt(
    system_prompt: str,
    user_prompt: str,
    response_model: Type[BaseModel],
    model: str = "gpt-4o-mini",
    temperature: float = 0.1,
) -> BaseModel:
    """
    Executes a structured prediction using OpenAI's response_format.
    If no OPENAI_API_KEY is found, runs in Mock Mode to facilitate demos.
    """
    client = get_llm_client()

    if not client:
        # MOCK MODE - returns empty/safe object for demonstration
        print(f"⚠️  [Mock Mode] OPENAI_API_KEY not found. Returning empty {response_model.__name__}.")
        # Construct a minimalist mock based on the schema's default/empty initializations
        from pydantic import create_model
        
        # A simple fallback for dev purposes. When we know the specific model, 
        # we can provide a better mock in the agent layer, but this fails safe.
        raise LLMError("Mock Mode requires explicit handling in the agent, or set OPENAI_API_KEY to run live.")

    try:
        completion = client.beta.chat.completions.parse(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            response_format=response_model,
            temperature=temperature,
        )
        
        result = completion.choices[0].message.parsed
        if not result:
            raise LLMError("LLM returned an empty parsed response.")
            
        return result
        
    except Exception as e:
        raise LLMError(f"Failed to execute LLM prompt: {str(e)}")
