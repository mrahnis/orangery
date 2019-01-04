import sys
import logging
from pkg_resources import iter_entry_points

import click
from click_plugins import with_plugins

import orangery

logger = logging.getLogger(__name__)


@with_plugins(iter_entry_points('orangery.subcommands'))
@click.option('-v', '--verbose', default=False, is_flag=True, help="Enables verbose mode")
@click.version_option(version=orangery.__version__, message='%(version)s')
@click.group()
@click.pass_context
def cli(ctx, verbose):
    ctx.obj = {}
    ctx.obj['verbose'] = verbose
    if verbose:
        logging.basicConfig(stream=sys.stderr, level=logging.INFO)
    else:
        logging.basicConfig(stream=sys.stderr, level=logging.ERROR)