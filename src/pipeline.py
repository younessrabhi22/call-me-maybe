from .function_selector import get_valid_next_tokens
from .argument_extractor import get_argument_ids



def generate_token_with_mask(model, current_text: str, allowed_token_ids: list[int]) -> int:

    """The Bouncer: Generates the next token limited to the `allowed_token_ids`."""

    input_ids = model.encode(current_text).squeeze(0).tolist()
    logits = model.get_logits_from_input_ids(input_ids)

    allowed_set = set(allowed_token_ids)

    for i in range(len(logits)):
        if i not in allowed_set:
            logits[i] = -float('inf')

    return logits.index(max(logits))



def update_state(current_text: str) -> str:

    """Reads the text generated so far and decides what state we are in."""

    if current_text.endswith("}}"):
        return "DONE"
    elif '"arguments":' in current_text:
        return "ARGUMENTS"
    elif '"name": "' in current_text and current_text.count('"') >= 4:
        return "ARGUMENTS"
    elif '"name": "' in current_text:
        return "CHOOSE_FUNCTION"
    elif "{" in current_text:
        return "NAME_KEY"
    return "START"


def generate_constrained_json(model, prompt: str, loaded_functions: list[dict]) -> str:


    current_text = prompt
    state = "START"

    print(f"\nProcessing prompt: '{prompt}'")

    while state != "DONE":

        if state == "START":
            vocab = model.get_vocab()
            vip_ids = [vocab.get("{", 0), vocab.get("Ġ{", 0)]

        elif state == "NAME_KEY":
            current_text += '\n  "name": "'
            state = "CHOOSE_FUNCTION"
            continue

        elif state == "CHOOSE_FUNCTION":
            current_value_typed = current_text.split('"name": "')[-1]
            allowed_strings = [func["name"] + '"' for func in loaded_functions]
            vip_ids = get_valid_next_tokens(model, current_value_typed, allowed_strings)
    
            if not vip_ids:
                current_text += ',\n  "arguments": {'
                state = "ARGUMENTS"
                continue

        elif state == "ARGUMENTS":
            vip_ids = get_argument_ids(model)

        best_token_id = generate_token_with_mask(model, current_text, vip_ids)
        winning_string = model.decode([best_token_id])
        current_text += winning_string
        state = update_state(current_text)

        if len(current_text) > len(prompt) + 1000:
            break

    return current_text
