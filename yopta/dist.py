import ast
import json
import re
import typing as tp
from pathlib import Path

BASE_PATH = Path().resolve()


def read_json(filename: str) -> dict:
    with open(filename, "r") as f:
        return json.load(f)


def read_file(filename: str):
    with open(filename, "r") as f:
        return f.read()


class Parser:
    def __init__(self):
        self.dictionary = read_json(
            "{path}/yopta/Resources/aliases.json".format(path=BASE_PATH)
        )
        self._yopta_code = None
        self._code = None

    def read(
        self, filepath: tp.Optional[str] = None, *, file: tp.Optional[tp.TextIO] = None
    ):
        if file is None:
            self._yopta_code = read_file(filepath)
        else:
            self._yopta_code = file.readlines()

    def compile(self):
        self.parse_yopta_to_python()

        if self._code is None:
            raise Exception()

        parsed_source = ast.parse(self._code)
        ast.fix_missing_locations(parsed_source)

        exec(compile(parsed_source, filename="<ast>", mode="exec"))

    def parse_yopta_to_python(self):
        _code = re.sub(
            "|".join(r"\b%s\b" % re.escape(s) for s in self.dictionary),
            self._replace,
            self._yopta_code,
        )
        tree = ast.parse(_code)
        self._code = tree

    def _replace(self, match):
        return self.dictionary[match.group(0)]


def yopta_compile(filename: str):
    parser = Parser()
    parser.read(filename)
    parser.compile()
