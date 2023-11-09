#!/usr/bin/env python3
import argparse
import inspect
from pathlib import Path
from pprint import pprint

from graphviz import Digraph

import yace.slang.parser


def grammar_get_rules(rules=None):
    rules = []
    for name, obj in inspect.getmembers(yace.slang.parser):
        if inspect.isfunction(obj) and name.startswith("p_"):
            doc = inspect.getdoc(obj)
            if doc:
                rules.append(doc)
    return rules


def grammar_as_graphviz(rules=None):
    rules = rules if rules else grammar_get_rules()

    dot = Digraph(comment="The BNF Grammar")

    for rule in rules:
        parts = rule.split(":")
        left = parts[0].strip()
        right = parts[1].strip()
        dot.node(left, left)
        for r in right.split():
            dot.node(r, r)
            dot.edge(left, r)

    dot.render("slang-grammar.gv", view=True)


def grammar_as_html(rules=None):
    rules = rules if rules else grammar_get_rules()

    html = "<html><head><style>"
    html += "body { font-family: Arial, sans-serif; }"
    html += ".rule { margin-bottom: 10px; }"
    html += ".rule-name { font-weight: bold; color: #333366; }"
    html += ".rule-def { color: #663333; }"
    html += "</style></head><body>"

    for rule in rules:
        parts = rule.split(":")
        left, right = parts[0].strip(), parts[1].strip()
        html += f'<div class="rule"><span class="rule-name">{left}</span> : <span class="rule-def">{right}</span></div>'

    html += "</body></html>"

    with Path("grammar.html").open("w") as foo:
        foo.write(html)


def cli_parse():
    """Returns command-line arguments"""

    parser = argparse.ArgumentParser(description="Yace See-Lang Lexer and Parser")

    parser.add_argument("filename", type=Path, help="The filename to process")

    return parser.parse_args()


def main():
    """Main entry-point"""

    args = cli_parse()

    with args.filename.open("r") as idlf:
        data = yace.slang.parser.get_parser().parse(idlf.read())

        pprint(data)
        grammar_as_graphviz()
        grammar_as_html()


if __name__ == "__main__":
    main()
