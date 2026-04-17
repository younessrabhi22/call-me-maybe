def get_valid_next_tokens(model, current_value_typed: str, allowed_full_strings: list[str]) -> list[int]:
    """
    Looks at what the AI has typed so far and filters the vocab tokens.
    Only allows tokens that build towards one of the `allowed_full_strings`.
    """
    vocab = model.get_vocab()
    vip_ids = []

    for token_string, token_id in vocab.items():
        clean_token = token_string.replace('Ġ', '')
        if not clean_token:
            continue

        potential_string = current_value_typed + clean_token

        is_safe_path = False
        for allowed_str in allowed_full_strings:
            if allowed_str.startswith(potential_string):
                is_safe_path = True
                break

        if is_safe_path:
            vip_ids.append(token_id)

    return vip_ids
