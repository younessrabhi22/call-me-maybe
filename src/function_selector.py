from llm_sdk import Small_LLM_Model


def generate_token_with_mask(
    model: Small_LLM_Model,
    current_text: str,
    allowed_token_ids: list[int]
) -> int:

    """Generate next token with masking."""

    input_ids = model.encode(current_text).tolist()[0]

    logits = model.get_logits_from_input_ids(input_ids)

    allowed_set = set(allowed_token_ids)

    for i in range(len(logits)):

        if i not in allowed_set:
            logits[i] = -float("inf")

    return logits.index(max(logits))


def select_function(
    prompt: str,
    fn_descriptions: str,
    function_names: list[str],
    model: Small_LLM_Model
) -> str:
    """Select best function."""

    context = (
        f"Available functions:\n"
        f"{fn_descriptions}\n\n"
        f"User request: {prompt}\n"
        f"Best function name: "
    )

    generated = ""

    candidates = function_names.copy()

    while len(candidates) > 1:

        allowed_token_ids = []

        for name in candidates:

            remaining = name.removeprefix(generated)

            token_ids = model.encode(remaining).tolist()[0]

            if token_ids:
                allowed_token_ids.append(token_ids[0])

        token_id = generate_token_with_mask(
            model,
            context + generated,
            allowed_token_ids
        )

        generated += model.decode([token_id])

        candidates = [name for name in candidates if name.startswith(generated)]

    return candidates[0]
