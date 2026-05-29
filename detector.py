def detect_local_issues(code):

    bugs = []
    warnings = []

    # Infinite loop detection
    if "while True" in code:
        warnings.append(
            "Possible infinite loop detected."
        )

    # SQL Injection
    if "SELECT * FROM" in code and "+" in code:
        bugs.append(
            "Possible SQL Injection vulnerability."
        )

    # Dangerous eval
    if "eval(" in code:
        bugs.append(
            "Use of eval() detected. This is dangerous."
        )

    # Missing recursion base case
    if "factorial(" in code and "if" not in code:
        warnings.append(
            "Recursive function may be missing base condition."
        )

    return {
        "bugs": bugs,
        "warnings": warnings
    }