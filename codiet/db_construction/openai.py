import json
from json.decoder import JSONDecodeError
import os

from openai import OpenAI

OPENAI_MODEL = "gpt-3.5-turbo"

def _get_openai_ingredient_description(ingredient_name: str) -> str:
    """Use the OpenAI API to generate a description for an ingredient."""
    # Initialize the OpenAI client
    client = OpenAI(api_key=os.environ.get("CODIET_OPENAI_API_KEY"))

    # Print an update
    print(f"Generating description for '{ingredient_name}'...")

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


def get_openai_ingredient_cost(
    ingredient_name: str, cost_data: dict
) -> dict[str, str | float]:
    """Use the OpenAI API to estimate the cost an ingredient."""

    print(f"Getting cost data for {ingredient_name}...")

    # Initialize the OpenAI client
    client = OpenAI(api_key=os.environ.get("CODIET_OPENAI_API_KEY"))

    prompt = f'''Can you respond to the prompt by filling in and returning the following dictionary of {ingredient_name}:
        "cost": {{
            "cost_unit": "GBP", # currency of the cost estimate
            "cost_value": null, # cost of the ingredient quantity
            "qty_value": null, # quantity of the ingredient
            "qty_unit": "g", # units used to measure ingredient quantity
        }}
    You'll need to return valid JSON because I need to parse it. It is acceptable to guess if you are not sure.'''

    completed = False
    while not completed:

        # Create a chat completion
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "user", "content": prompt},
            ],
            model=OPENAI_MODEL,
        )

        # Grab the response
        response = chat_completion.choices[0].message.content  # type: ignore

        # Check the response and populate the output dict
        try:
            # Convert the response to a dict
            raw_cost_data = json.loads(response)  # type: ignore
            # Init a processed cost data dict
            cost_data = {"cost_unit": "GBP"}
            # Check the fields are populated correctly
            cost_data["cost_value"] = float(raw_cost_data["cost"]["cost_value"])
            cost_data["qty_value"] = float(raw_cost_data["cost"]["qty_value"])
            cost_data["qty_unit"] = str(raw_cost_data["cost"]["qty_unit"])

            # Check the qty unit is on the approve list
            # TODO: Ultimately, these will come from the database.
            if cost_data["qty_unit"] not in ["g", "kg", "ml", "l"]:
                raise ValueError

        except JSONDecodeError:
            print(f"Retrying {ingredient_name} cost due to JSONDecodeError")
            continue
        except KeyError:
            print(f"Retrying {ingredient_name} cost due to KeyError")
            continue
        except ValueError:
            print(f"Retrying {ingredient_name} cost due to ValueError")
            continue

        completed = True
    return cost_data

def get_openai_ingredient_flags(
    ingredient_name: str, flag_list: list[str]
) -> dict[str, bool]:
    """Use the OpenAI API to generate a list of flags for an ingredient."""
    print(f"Getting flags for {ingredient_name}...")

    # Initialize the OpenAI client
    client = OpenAI(api_key=os.environ.get("CODIET_OPENAI_API_KEY"))

    # Construct the flag dict with False values
    flags_dict = {flag: None for flag in flag_list}

    # Set the prompt
    prompt = f"Can you set each of these flags to True of False for {ingredient_name}: {json.dumps(flags_dict, indent=4)}? If unsure, choose False. Reply with JSON only"

    completed = False
    while not completed:

        # Create a chat completion
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "user", "content": prompt},
            ],
            model=OPENAI_MODEL,
        )

        # Grab the response
        response = chat_completion.choices[0].message.content  # type: ignore

        # Check the response and populate the output dict
        output_dict = {}
        try:
            # Convert the response to a dict
            flags_dict = json.loads(response)  # type: ignore

            # Check that there are the same number of fields in the response as in the flag list
            if len(flags_dict) != len(flag_list):
                raise KeyError
            
            # Check that each field in the response is in the flag list
            for flag in flags_dict:
                if flag not in flag_list:
                    raise KeyError
                
            # Check that each field in the response is a boolean
            for flag in flags_dict:
                if not isinstance(flags_dict[flag], bool):
                    raise ValueError
                
            # Populate the output dict
            output_dict = flags_dict

        except JSONDecodeError:
            print(f"Retrying {ingredient_name} flags due to JSONDecodeError")
            continue
        except ValueError:
            print(f"Retrying {ingredient_name} flags due to ValueError")
            continue
        except KeyError:
            print(f"Retrying {ingredient_name} flags due to KeyError")
            continue
        
        completed = True

    return output_dict


def get_openai_ingredient_gi(ingredient_name: str) -> float:
    """Use the OpenAI API to generate a description for an ingredient."""
    print(f"Getting GI for {ingredient_name}...")
    # Initialize the OpenAI client
    client = OpenAI(api_key=os.environ.get("CODIET_OPENAI_API_KEY"))

    # Set the prompt
    prompt = f"By responding with a single decimal only, what is the approximate Glycemic Index (GI) of '{ingredient_name}'? Approximate values are OK."

    completed = False
    while not completed:

        # Create a chat completion
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "user", "content": prompt},
            ],
            model=OPENAI_MODEL,
        )

        # Grab the response
        response = chat_completion.choices[0].message.content

        try:
            # Check the response is a float
            gi = float(response) # type: ignore

            # Check the response is in the correct range
            if gi < 0 or gi > 100:
                raise ValueError

        except ValueError:
            print(f"Retrying {ingredient_name} GI due to ValueError")
            continue

        completed = True
    
    return gi

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