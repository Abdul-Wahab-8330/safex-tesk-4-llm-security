from .config import DEFENDED_SYSTEM_PROMPT
from .input_guard import validate_input
from .llm_client import generate_response
from .output_guard import validate_output


def defended_ask_llm(
    user_input,
    client=None,
    model_name=None,
):
    """
    Process input through the security pipeline.

    Status values:
    - blocked_input
    - blocked_output
    - success
    - api_error
    """
    input_check = validate_input(user_input)

    if not input_check["allowed"]:
        return {
            "status": "blocked_input",
            "reason": input_check["reason"],
            "response": None,
        }

    try:
        output_text = generate_response(
            prompt=user_input,
            system_instruction=DEFENDED_SYSTEM_PROMPT,
            client=client,
            model_name=model_name,
        )

        output_check = validate_output(output_text)

        if not output_check["safe"]:
            return {
                "status": "blocked_output",
                "reason": output_check["reason"],
                "response": None,
            }

        return {
            "status": "success",
            "reason": "passed_known_checks",
            "response": output_text,
        }

    except Exception as exc:
        # Keep API/service failures separate from security blocks.
        return {
            "status": "api_error",
            "reason": f"{type(exc).__name__}: {exc}",
            "response": None,
        }