#!/usr/bin/env python
# coding=utf-8

# IMPORT ALL PACKAGES
from shuttle import __version__
from shuttle.cli import click
# IMPORT PROVIDERS
from shuttle.cli.providers.bitcoin import bitcoin
from shuttle.cli.providers.bytom import bytom

CONTEXT_SETTINGS = dict(
    help_option_names=["-h", "--help"],
)


class AliasedGroup(click.Group):

    def get_command(self, ctx, cmd_name):
        rv = click.Group.get_command(self, ctx, cmd_name)
        if rv is not None:
            return rv
        matches = [x for x in self.list_commands(ctx)
                   if x.startswith(cmd_name)]
        if not matches:
            return None
        elif len(matches) == 1:
            return click.Group.get_command(self, ctx, matches[0])
        ctx.fail('Too many matches: %s' % ', '.join(sorted(matches)))


def print_version(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    click.echo("v%s" % __version__)
    ctx.exit()


@click.group(cls=AliasedGroup,
             options_metavar="[OPTIONS]", context_settings=CONTEXT_SETTINGS)
@click.option("-v", "--version", is_flag=True, callback=print_version,
              expose_value=False, help="Show Shuttle version and exit.")
def main():
    pass


# Adding bitcoin provider
main.add_command(bitcoin)
# Adding bytom provider
main.add_command(bytom)
