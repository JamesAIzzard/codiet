import json
import os

import openai as OpenAI

OPENAI_MODEL = "gpt-3.5-turbo"

def _get_openai_ingredient_description(ingredient_name: str) -> str:
    """Use the OpenAI API to generate a description for an ingredient."""
    # Initialize the OpenAI client
    client = OpenAI(api_key=os.environ.get("CODIET_OPENAI_API_KEY"))

    # Set the prompt
    prompt = f"Generate a single sentence description for the ingredient '{ingredient_name}'."

    # Create a chat completion
    chat_completion = client.chat.completions.create(
        messages=[
            {"role": "user", "content": prompt},
        ],
        model=OPENAI_MODEL,
    )

    return chat_completion.choices[0].message.content  # type: ignore


def _get_openai_ingredient_cost(
    ingredient_name: str, cost_data: dict
) -> dict[str, str | float]:
    """Use the OpenAI API to generate a description for an ingredient."""
    # Initialize the OpenAI client
    client = OpenAI(api_key=os.environ.get("CODIET_OPENAI_API_KEY"))

    # Set the prompt
    prompt = fprompt = (
        f"Can you populate this cost data for {ingredient_name}: {json.dumps(cost_data, indent=4)}? Guessing is OK."
    )

    # Create a chat completion
    chat_completion = client.chat.completions.create(
        messages=[
            {"role": "user", "content": prompt},
        ],
        model=OPENAI_MODEL,
    )

    # Parse the response
    response = chat_completion.choices[0].message.content  # type: ignore

    # Convert the response to a dict
    return json.loads(response)  # type: ignore


def _get_openai_ingredient_flags(
    ingredient_name: str, flag_list: list[str]
) -> dict[str, bool]:
    """Use the OpenAI API to generate a list of flags for an ingredient."""
    # Initialize the OpenAI client
    client = OpenAI(api_key=os.environ.get("CODIET_OPENAI_API_KEY"))

    # Construct the flag dict with False values
    flags_dict = {flag: False for flag in flag_list}

    # Set the prompt
    prompt = f"Can you populate this list of flags for {ingredient_name}: {json.dumps(flags_dict, indent=4)}? If unsure, leave flag as False."
    # prompt = f"Generate a list of flags for the ingredient '{ingredient_name}'."

    # Create a chat completion
    chat_completion = client.chat.completions.create(
        messages=[
            {"role": "user", "content": prompt},
        ],
        model=OPENAI_MODEL,
    )

    # Parse the response
    response = chat_completion.choices[0].message.content  # type: ignore
    # Convert the response to a dict
    flags_dict = json.loads(response)  # type: ignore

    return flags_dict


def _get_openai_ingredient_gi(ingredient_name: str) -> str:
    """Use the OpenAI API to generate a description for an ingredient."""
    # Initialize the OpenAI client
    client = OpenAI(api_key=os.environ.get("CODIET_OPENAI_API_KEY"))

    # Set the prompt
    prompt = f"By responding with a single decimal only, what is the approximate Glycemic Index (GI) of '{ingredient_name}'? Guessing is OK."

    # Create a chat completion
    chat_completion = client.chat.completions.create(
        messages=[
            {"role": "user", "content": prompt},
        ],
        model=OPENAI_MODEL,
    )

    return chat_completion.choices[0].message.content  # type: ignore

def _get_openai_ingredient_nutrients(
    ingredient_name: str, nutrient_data: dict[str, dict[str, str | float]]
) -> dict[str, dict[str, str | float]]:
    """Use the OpenAI API to generate nutrient data for an ingredient."""
    # Initialize the OpenAI client
    client = OpenAI(api_key=os.environ.get("CODIET_OPENAI_API_KEY"))

    # Set the prompt
    prompt = f"Can you populate this nutrient data for {ingredient_name}: {json.dumps(nutrient_data, indent=4)}? Provide a guess if unsure. Reply with JSON only."

    # Create a chat completion
    chat_completion = client.chat.completions.create(
        messages=[
            {"role": "user", "content": prompt},
        ],
        model=OPENAI_MODEL,
    )

    # Parse the response
    response = json.loads(chat_completion.choices[0].message.content)  # type: ignore

    return response