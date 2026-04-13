import json
from llm_sdk import Small_LLM_Model
import torch


def load_vocabulary(model: Small_LLM_Model) -> tuple[dict, dict]:

    """Loads vocab in both directions.

    Returns:
        token_str -> id  (for encoding)
        id -> token_str  (for decoding during constrained generation)
    """

    vocab_path = model.get_path_to_vocab_file()

    with open(vocab_path, "r", encoding="utf-8") as f:
        str_to_id: dict = json.load(f)

    id_to_str: dict = {v: k for k, v in str_to_id.items()}

    return str_to_id, id_to_str



def generate_token_with_mask(model, current_text: str, allowed_token_ids: list[int]) -> int:
    """
    Generates the next token, strictly limited to the `allowed_token_ids`.
    """
    input_ids = model.encode(current_text).squeeze(0).tolist()
    logits = model.get_logits_from_input_ids(input_ids)

    allowed_set = set(allowed_token_ids)

    for i in range(len(logits)):
        if i not in allowed_set:
            logits[i] = -float('inf')

    best_token_id = logits.index(max(logits))

    return best_token_id
