
def get_argument_ids(model) -> list[int]:
    """
    Scans the AI's entire vocabulary and returns the Token IDs
    for tokens that are entirely made of safe JSON characters.
    """
    vocab = model.get_vocab()
    safe_chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_."-:, {}[]'

    vip_ids = []

    for token_string, token_id in vocab.items():
        clean_token = token_string.replace('Ġ', '')
        if not clean_token:
            continue

        is_safe = True
        for char in clean_token:
            if char not in safe_chars:
                is_safe = False
                break

        if is_safe:
            vip_ids.append(token_id)

    return vip_ids
