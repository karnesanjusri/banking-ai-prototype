"""
demo.py

Command-line demo for the Banking AI Case Study prototype.

Usage:
    python demo.py                          -> runs a few built-in sample messages
    python demo.py "My card hasn't arrived"  -> classifies your own message
    python demo.py --interactive             -> type messages one at a time, Ctrl+C to quit
"""

import json
import sys

from classifier import IntentClassifier

SAMPLE_MESSAGES = [
    "My card hasn't arrived yet.",
    "I made a transfer yesterday but the money still hasn't reached the recipient.",
    "why was I charged for withdrawing cash",
    "I want to close my account",
    "asdkjh random gibberish text 12345",  # meant to show a low-confidence case
]


def print_result(message: str, result: dict) -> None:
    print(f"\nCustomer message: {message!r}")
    print(json.dumps(result, indent=2))


def main() -> None:
    print("Loading classifier (training on BANKING77 data)...")
    clf = IntentClassifier()
    print("Ready.\n" + "-" * 50)

    args = sys.argv[1:]

    if args and args[0] == "--interactive":
        print("Interactive mode. Type a customer message and press Enter.")
        print("Press Ctrl+C to quit.\n")
        try:
            while True:
                message = input("Customer message> ").strip()
                if not message:
                    continue
                print_result(message, clf.classify(message))
        except (KeyboardInterrupt, EOFError):
            print("\nGoodbye.")
        return

    if args:
        message = " ".join(args)
        print_result(message, clf.classify(message))
        return

    # No arguments: run the built-in samples
    for message in SAMPLE_MESSAGES:
        print_result(message, clf.classify(message))
    print("-" * 50)
    print("Tip: run 'python demo.py \"your own message\"' to try your own input,")
    print("or 'python demo.py --interactive' to try several in a row.")


if __name__ == "__main__":
    main()
