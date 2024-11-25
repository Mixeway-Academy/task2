def mask_string(input_str: str, mask_char: str = "X") -> str:
    """
    Converts input string to a string of mask characters of the same length.

    Args:
        input_str: String to mask
        mask_char: Character to use for masking (default: "X")

    Returns:
        Masked string of the same length as input

    Examples:
        >>> mask_string("12345")
        'XXXXX'
        >>> mask_string("hello", "*")
        '*****'
    """
    if not input_str:
        return input_str

    if len(mask_char) != 1:
        raise ValueError("mask_char must be a single character")

    return mask_char * len(input_str)