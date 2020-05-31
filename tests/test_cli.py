from pkg_resources import iter_entry_points

from click.testing import CliRunner


import orangery
from orangery.cli.orangery import cli


def test_orangery():
    runner = CliRunner()
    result = runner.invoke(cli, ['--help'])
    assert result.exit_code == 0


def test_adjust():
    runner = CliRunner()
    result = runner.invoke(cli, ['adjust', '--help'])
    assert result.exit_code == 0


def test_info():
    runner = CliRunner()
    result = runner.invoke(cli, ['info', '--help'])
    assert result.exit_code == 0


def test_section():
    runner = CliRunner()
    result = runner.invoke(cli, ['section', '--help'])
    assert result.exit_code == 0


def test_segment():
    runner = CliRunner()
    result = runner.invoke(cli, ['segment', '--help'])
    assert result.exit_code == 0
