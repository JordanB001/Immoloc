
def remove_star(text_with_star: str) -> str:
    if not isinstance(text_with_star, str):
        raise TypeError("Input must be a string")
    if text_with_star == "":
        raise ValueError("Input string is empty")
    return text_with_star.replace('*', '')

#print(remove_star("* BLBA **TITRE** tqsfs"))    
    
    