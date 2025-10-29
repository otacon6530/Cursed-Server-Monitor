#!/usr/bin/env python3
import click

@click.group()
def cli():
    pass

from commands.test import test
cli.add_command(test)

from commands.start import start
cli.add_command(start)

if __name__ == "__main__":
    cli()
