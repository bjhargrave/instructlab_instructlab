# SPDX-License-Identifier: Apache-2.0

# pylint: disable=too-many-lines

# Standard
import logging
import multiprocessing
import typing

# Third Party
from click_didyoumean import DYMGroup
import click

# First Party
from instructlab import config

# Local
from .configuration import config as config_group
from .data import data as data_group

# NOTE: Subcommands are using local imports to speed up startup time.
from .model import model as model_group
from .sysinfo import get_sysinfo
from .taxonomy import taxonomy as taxonomy_group

# 'fork' is unsafe and incompatible with some hardware accelerators.
# Python 3.14 will switch to 'spawn' on all platforms.
multiprocessing.set_start_method(
    config.DEFAULT_MULTIPROCESSING_START_METHOD, force=True
)

# Set logging level of OpenAI client and httpx library to ERROR to suppress INFO messages
logging.getLogger("openai").setLevel(logging.ERROR)
logging.getLogger("httpx").setLevel(logging.ERROR)

if typing.TYPE_CHECKING:
    # Third Party
    import torch


@click.group(cls=DYMGroup)
@click.option(
    "--config",
    "config_file",
    type=click.Path(),
    default=config.DEFAULT_CONFIG,
    show_default=True,
    help="Path to a configuration file.",
)
@click.version_option(package_name="instructlab")
@click.pass_context
# pylint: disable=redefined-outer-name
def ilab(ctx, config_file):
    """CLI for interacting with InstructLab.

    If this is your first time running ilab, it's best to start with `ilab init` to create the environment.
    """
    config.init_config(ctx, config_file)


ilab.add_command(model_group.model)
ilab.add_command(taxonomy_group.taxonomy)
ilab.add_command(data_group.data)
ilab.add_command(config_group.config)


@ilab.command
def sysinfo():
    """Print system information"""
    for key, value in get_sysinfo().items():
        print(f"{key}: {value}")
