def hide_sensitive_data(data: str) -> str:
    hidden = ""
    for char in data:
        if char not in ["/", " ", "_"]:
            hidden = hidden + "*"
        else:
            hidden = hidden + char
            
    return hidden