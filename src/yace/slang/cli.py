#!/usr/bin/env python3
import argparse
from pathlib import Path

from yace.slang.parser import get_lexer


def cli_parse():
    """Returns command-line arguments"""

    parser = argparse.ArgumentParser(description="Yace See-Lang Lexer and Parser")

    parser.add_argument("filename", type=Path, help="The filename to process")

    return parser.parse_args()


def main():
    """Main entry-point"""

    args = cli_parse()

    lexer = get_lexer()

    with args.filename.open("r") as idlf:
        lexer.input(idlf.read())

    while True:
        tok = lexer.token()
        if not tok:
            break
        print(tok)


if __name__ == "__main__":
    main()
