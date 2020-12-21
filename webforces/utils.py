def remove_empty_lines(s: str) -> str:
    return '\n'.join([line.strip() for line in s.split('\n') if line.strip()])
