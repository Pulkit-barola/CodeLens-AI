def calculate_quality_metrics(code):
    """Calculate readability, maintainability, performance, and security scores."""

    code_lower = code.lower()
    lines = len(code.splitlines())

    readability    = 100
    maintainability = 100
    performance    = 100
    security       = 100

    # --- Readability ---
    if lines > 50:
        readability -= 10
    if lines > 100:
        readability -= 15
    if len(code) > 3000:
        readability -= 10

    # --- Maintainability ---
    if code.count("if") > 5:
        maintainability -= 10
    if code.count("for") > 5:
        maintainability -= 10
    if code.count("while") > 3:
        maintainability -= 10
    if "try:" not in code and "except" not in code:
        maintainability -= 5

    # --- Performance ---
    if "while true" in code_lower:
        performance -= 25
    if "sleep(" in code_lower:
        performance -= 5
    if "factorial(" in code_lower:
        performance -= 5
    if "fibonacci(" in code_lower:
        performance -= 5

    # --- Security ---
    if "eval(" in code_lower:
        security -= 40
    if "exec(" in code_lower:
        security -= 40
    if "os.system(" in code_lower:
        security -= 25
    if "subprocess.call(" in code_lower:
        security -= 20

    # Clamp all values to [0, 100]
    readability     = max(0, min(100, readability))
    maintainability = max(0, min(100, maintainability))
    performance     = max(0, min(100, performance))
    security        = max(0, min(100, security))

    overall = int((readability + maintainability + performance + security) / 4)

    return {
        "overall":        overall,
        "readability":    readability,
        "maintainability": maintainability,
        "performance":    performance,
        "security":       security
    }


def analyze_complexity(code):
    """Estimate time/space complexity and difficulty level."""

    code_lower = code.lower()

    time_complexity  = "O(1)"
    space_complexity = "O(1)"
    level            = "Easy"

    loop_count = code_lower.count("for ") + code_lower.count("while ")

    if loop_count >= 2:
        time_complexity = "O(n²)"
        level = "Hard"
    elif loop_count == 1:
        time_complexity = "O(n)"
        level = "Medium"

    if "factorial(" in code_lower or "fibonacci(" in code_lower:
        time_complexity = "O(n)"
        level = "Medium"

    # Recursive Fibonacci is exponential
    if "fibonacci(" in code_lower:
        time_complexity = "O(2ⁿ)"
        level = "Very Hard"

    if "[]" in code or "list(" in code_lower:
        space_complexity = "O(n)"

    return {
        "time":  time_complexity,
        "space": space_complexity,
        "level": level
    }
