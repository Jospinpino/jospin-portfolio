"""Password Strength Checker, a fully offline command line tool.

Scores a password on length, character variety, and known weak patterns
(common passwords, sequences, repeated characters). Nothing is sent over
the network and nothing is written to disk.
"""

import argparse
import getpass
import math
import re
import sys

from common_passwords import COMMON_PASSWORDS

SEQUENCES = [
    "0123456789", "abcdefghijklmnopqrstuvwxyz", "qwertyuiop", "asdfghjkl", "zxcvbnm",
]


def charset_size(password):
    size = 0
    if re.search(r"[a-z]", password):
        size += 26
    if re.search(r"[A-Z]", password):
        size += 26
    if re.search(r"[0-9]", password):
        size += 10
    if re.search(r"[^a-zA-Z0-9]", password):
        size += 33
    return size or 1


def has_sequence(password, min_run=4):
    lowered = password.lower()
    for seq in SEQUENCES:
        for start in range(len(seq) - min_run + 1):
            chunk = seq[start:start + min_run]
            if chunk in lowered or chunk[::-1] in lowered:
                return True
    return False


def has_repeated_run(password, min_run=4):
    return bool(re.search(r"(.)\1{" + str(min_run - 1) + r",}", password))


def analyze(password):
    issues = []
    length = len(password)

    if length == 0:
        return {
            "score": 0,
            "label": "Empty",
            "entropy_bits": 0.0,
            "issues": ["The password is empty."],
        }

    entropy_bits = length * math.log2(charset_size(password))

    if length < 8:
        issues.append("Shorter than 8 characters.")
    if not re.search(r"[a-z]", password):
        issues.append("No lowercase letters.")
    if not re.search(r"[A-Z]", password):
        issues.append("No uppercase letters.")
    if not re.search(r"[0-9]", password):
        issues.append("No digits.")
    if not re.search(r"[^a-zA-Z0-9]", password):
        issues.append("No symbols.")
    if password.lower() in COMMON_PASSWORDS:
        issues.append("This is one of the most common passwords in use, avoid it entirely.")
    if has_sequence(password):
        issues.append("Contains an obvious sequence (like '1234' or 'qwerty').")
    if has_repeated_run(password):
        issues.append("Contains a long run of the same character.")

    score = 0
    if length >= 8:
        score += 1
    if length >= 12:
        score += 1
    if length >= 16:
        score += 1
    if re.search(r"[a-z]", password) and re.search(r"[A-Z]", password):
        score += 1
    if re.search(r"[0-9]", password):
        score += 1
    if re.search(r"[^a-zA-Z0-9]", password):
        score += 1
    if password.lower() in COMMON_PASSWORDS:
        score = 0
    if has_sequence(password) or has_repeated_run(password):
        score = max(0, score - 2)

    score = max(0, min(score, 6))
    labels = {
        0: "Very Weak", 1: "Very Weak", 2: "Weak",
        3: "Fair", 4: "Good", 5: "Strong", 6: "Very Strong",
    }

    return {
        "score": score,
        "label": labels[score],
        "entropy_bits": round(entropy_bits, 1),
        "issues": issues,
    }


def print_report(password, result):
    bar_length = 20
    filled = round((result["score"] / 6) * bar_length)
    bar = "#" * filled + "." * (bar_length - filled)

    print(f"Strength: {result['label']} [{bar}] ({result['score']}/6)")
    print(f"Estimated entropy: {result['entropy_bits']} bits")

    if result["issues"]:
        print("\nSuggestions:")
        for issue in result["issues"]:
            print(f"  - {issue}")
    else:
        print("\nNo issues found, this looks like a solid password.")


def main():
    parser = argparse.ArgumentParser(
        description="Check a password's strength entirely offline, nothing leaves your machine."
    )
    parser.add_argument(
        "--password",
        help="Password to check (visible in shell history, prefer the interactive prompt)",
    )
    args = parser.parse_args()

    password = args.password
    if password is None:
        try:
            password = getpass.getpass("Password to check (hidden input): ")
        except (KeyboardInterrupt, EOFError):
            print("\nCancelled.")
            sys.exit(1)

    result = analyze(password)
    print_report(password, result)


if __name__ == "__main__":
    main()
