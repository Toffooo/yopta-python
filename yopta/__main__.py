import os
from pathlib import Path

import click
from dist import yopta_compile

BASE_PATH = Path().resolve()


@click.group()
@click.version_option("1.0.0")
def main():
    pass


@main.command()
@click.argument("keyword", required=False)
def run(**kwargs):
    yopta_compile(filename=os.path.join(BASE_PATH, kwargs["keyword"]))


if __name__ == "__main__":
    main()
